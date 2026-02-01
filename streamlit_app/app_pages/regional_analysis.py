"""
Regional Analysis - Sales performance by geographic region
"""
import streamlit as st
from datetime import timedelta
import pandas as pd

conn = st.session_state.conn
date_start = st.session_state.date_start
date_end = st.session_state.date_end

st.title(":material/map: Regional Analysis")

@st.cache_data(ttl=timedelta(minutes=5))
def get_regional_data(_conn, start_date, end_date):
    """Fetch regional sales data by month."""
    query = f"""
    SELECT 
        ORDER_REGION as REGION,
        DATE_TRUNC('month', ORDER_DATE) as ORDER_MONTH,
        SUM(NET_AMOUNT) as REVENUE,
        COUNT(*) as ORDER_COUNT,
        COUNT(DISTINCT CUSTOMER_ID) as CUSTOMER_COUNT,
        AVG(NET_AMOUNT) as AVG_ORDER_VALUE
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY ORDER_REGION, DATE_TRUNC('month', ORDER_DATE)
    ORDER BY ORDER_MONTH, REGION
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_regional_summary(_conn, start_date, end_date):
    """Fetch regional summary totals."""
    query = f"""
    SELECT 
        ORDER_REGION as REGION,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as TOTAL_ORDERS,
        COUNT(DISTINCT CUSTOMER_ID) as TOTAL_CUSTOMERS,
        ROUND(AVG(NET_AMOUNT), 2) as AVG_ORDER_VALUE
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY ORDER_REGION
    ORDER BY TOTAL_REVENUE DESC
    """
    return _conn.query(query)

# Load data with error handling and loading state
data_loaded = False
regional_data = pd.DataFrame()
regional_summary = pd.DataFrame()

with st.spinner("Loading regional data..."):
    try:
        regional_data = get_regional_data(conn, date_start, date_end)
        regional_summary = get_regional_summary(conn, date_start, date_end)
        data_loaded = True
    except Exception as e:
        st.error(f"Failed to load regional data: {str(e)}")

# Region selector
if data_loaded and len(regional_summary) > 0:
    regions = regional_summary['REGION'].tolist()
    selected_regions = st.multiselect(
        "Select Regions",
        options=regions,
        default=regions
    )
    
    # Filter data
    filtered_summary = regional_summary[regional_summary['REGION'].isin(selected_regions)]
    filtered_trend = regional_data[regional_data['REGION'].isin(selected_regions)]
    
    # KPI cards by region
    st.subheader("Regional Performance")
    cols = st.columns(len(selected_regions))
    for i, region in enumerate(selected_regions):
        region_row = filtered_summary[filtered_summary['REGION'] == region]
        if len(region_row) > 0:
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"**{region}**")
                    rev = region_row['TOTAL_REVENUE'].iloc[0]
                    orders = region_row['TOTAL_ORDERS'].iloc[0]
                    st.metric("Revenue", f"${rev:,.0f}")
                    st.metric("Orders", f"{orders:,}")
    
    # Charts
    st.subheader("Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**Monthly Revenue by Region**")
            if len(filtered_trend) > 0:
                pivot_data = filtered_trend.pivot(index='ORDER_MONTH', columns='REGION', values='REVENUE')
                st.line_chart(pivot_data, height=350)
    
    with col2:
        with st.container(border=True):
            st.markdown("**Revenue Distribution**")
            st.bar_chart(filtered_summary, x="REGION", y="TOTAL_REVENUE", height=350)
    
    # Data table
    st.subheader("Regional Summary")
    with st.container(border=True):
        st.dataframe(
            filtered_summary,
            hide_index=True,
            column_config={
                "TOTAL_REVENUE": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                "TOTAL_ORDERS": st.column_config.NumberColumn("Orders", format="%d"),
                "TOTAL_CUSTOMERS": st.column_config.NumberColumn("Customers", format="%d"),
                "AVG_ORDER_VALUE": st.column_config.NumberColumn("Avg Order", format="$%.2f"),
            },
            use_container_width=True
        )
elif data_loaded:
    st.info("No regional data available for selected period")
