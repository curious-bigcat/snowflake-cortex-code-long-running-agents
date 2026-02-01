"""
Sales Rep Leaderboard - Performance rankings and metrics
"""
import streamlit as st
from datetime import timedelta
import pandas as pd

conn = st.session_state.conn
date_start = st.session_state.date_start
date_end = st.session_state.date_end

st.title(":material/leaderboard: Sales Rep Leaderboard")

@st.cache_data(ttl=timedelta(minutes=5))
def get_rep_rankings(_conn, start_date, end_date):
    """Fetch sales rep performance rankings."""
    query = f"""
    SELECT 
        REP_NAME,
        REP_REGION as REGION,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as TOTAL_ORDERS,
        COUNT(DISTINCT CUSTOMER_ID) as TOTAL_CUSTOMERS,
        ROUND(AVG(NET_AMOUNT), 2) as AVG_ORDER_VALUE
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY REP_NAME, REP_REGION
    ORDER BY TOTAL_REVENUE DESC
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_rep_trend(_conn, start_date, end_date, rep_name):
    """Fetch monthly trend for a specific rep."""
    query = f"""
    SELECT 
        DATE_TRUNC('month', ORDER_DATE) as MONTH,
        SUM(NET_AMOUNT) as REVENUE,
        COUNT(*) as ORDER_COUNT,
        COUNT(DISTINCT CUSTOMER_ID) as CUSTOMER_COUNT
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE REP_NAME = '{rep_name}'
      AND ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE_TRUNC('month', ORDER_DATE)
    ORDER BY MONTH
    """
    return _conn.query(query)

# Load rankings with error handling and loading state
data_loaded = False
rankings = pd.DataFrame()

with st.spinner("Loading sales rep data..."):
    try:
        rankings = get_rep_rankings(conn, date_start, date_end)
        data_loaded = True
    except Exception as e:
        st.error(f"Failed to load sales rep data: {str(e)}")

if data_loaded and len(rankings) > 0:
    # Add rank column
    rankings['RANK'] = range(1, len(rankings) + 1)
    
    # Region filter
    regions = rankings['REGION'].unique().tolist()
    selected_region = st.selectbox("Filter by Region", ["All Regions"] + regions)
    
    if selected_region != "All Regions":
        filtered = rankings[rankings['REGION'] == selected_region].copy()
        filtered['RANK'] = range(1, len(filtered) + 1)
    else:
        filtered = rankings
    
    # Top 3 podium
    st.subheader("Top Performers")
    top3 = filtered.head(3)
    
    if len(top3) >= 3:
        cols = st.columns([1, 1.2, 1])
        
        # Second place
        with cols[0]:
            with st.container(border=True):
                st.markdown("### 🥈 #2")
                st.markdown(f"**{top3.iloc[1]['REP_NAME']}**")
                st.metric("Revenue", f"${top3.iloc[1]['TOTAL_REVENUE']:,.0f}")
        
        # First place
        with cols[1]:
            with st.container(border=True):
                st.markdown("### 🥇 #1")
                st.markdown(f"**{top3.iloc[0]['REP_NAME']}**")
                st.metric("Revenue", f"${top3.iloc[0]['TOTAL_REVENUE']:,.0f}")
        
        # Third place
        with cols[2]:
            with st.container(border=True):
                st.markdown("### 🥉 #3")
                st.markdown(f"**{top3.iloc[2]['REP_NAME']}**")
                st.metric("Revenue", f"${top3.iloc[2]['TOTAL_REVENUE']:,.0f}")
    
    # Full leaderboard
    st.subheader("Full Leaderboard")
    with st.container(border=True):
        st.dataframe(
            filtered[['RANK', 'REP_NAME', 'REGION', 'TOTAL_REVENUE', 'TOTAL_ORDERS', 'TOTAL_CUSTOMERS', 'AVG_ORDER_VALUE']],
            hide_index=True,
            column_config={
                "RANK": st.column_config.NumberColumn("#", width="small"),
                "REP_NAME": "Sales Rep",
                "REGION": "Region",
                "TOTAL_REVENUE": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                "TOTAL_ORDERS": st.column_config.NumberColumn("Orders", format="%d"),
                "TOTAL_CUSTOMERS": st.column_config.NumberColumn("Customers", format="%d"),
                "AVG_ORDER_VALUE": st.column_config.NumberColumn("AOV", format="$%.2f"),
            },
            use_container_width=True,
            height=400
        )
    
    # Individual rep detail
    st.subheader("Rep Detail")
    selected_rep = st.selectbox("Select Rep", filtered['REP_NAME'].tolist())
    
    if selected_rep:
        try:
            rep_trend = get_rep_trend(conn, date_start, date_end, selected_rep)
            rep_info = filtered[filtered['REP_NAME'] == selected_rep].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown(f"**{selected_rep}** - {rep_info['REGION']}")
                    st.metric("Total Revenue", f"${rep_info['TOTAL_REVENUE']:,.0f}")
                    st.metric("Total Orders", f"{rep_info['TOTAL_ORDERS']:,}")
                    st.metric("Avg Order Value", f"${rep_info['AVG_ORDER_VALUE']:,.2f}")
            
            with col2:
                with st.container(border=True):
                    st.markdown("**Monthly Trend**")
                    if len(rep_trend) > 0:
                        st.line_chart(rep_trend, x="MONTH", y="REVENUE", height=250)
        except Exception as e:
            st.warning(f"Could not load rep details: {str(e)}")
elif data_loaded:
    st.info("No sales rep data available for selected period")
