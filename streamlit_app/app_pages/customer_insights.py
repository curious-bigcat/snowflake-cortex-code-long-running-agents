"""
Customer Insights - Customer segmentation and analysis
"""
import streamlit as st
from datetime import timedelta
import pandas as pd

conn = st.session_state.conn
date_start = st.session_state.date_start
date_end = st.session_state.date_end

st.title(":material/groups: Customer Insights")

@st.cache_data(ttl=timedelta(minutes=5))
def get_segment_summary(_conn, start_date, end_date):
    """Fetch summary by customer segment."""
    query = f"""
    SELECT 
        CUSTOMER_SEGMENT as SEGMENT,
        COUNT(DISTINCT CUSTOMER_ID) as CUSTOMER_COUNT,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as ORDER_COUNT,
        AVG(NET_AMOUNT) as AVG_ORDER_VALUE
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY CUSTOMER_SEGMENT
    ORDER BY TOTAL_REVENUE DESC
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_top_customers(_conn, start_date, end_date, limit=25):
    """Fetch top customers by revenue."""
    query = f"""
    SELECT 
        CUSTOMER_NAME,
        CUSTOMER_SEGMENT as SEGMENT,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as ORDER_COUNT,
        ROUND(AVG(NET_AMOUNT), 2) as AVG_ORDER_VALUE,
        MIN(ORDER_DATE) as FIRST_ORDER_DATE,
        MAX(ORDER_DATE) as LAST_ORDER_DATE
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY CUSTOMER_NAME, CUSTOMER_SEGMENT
    ORDER BY TOTAL_REVENUE DESC
    LIMIT {limit}
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_industry_breakdown(_conn, start_date, end_date):
    """Fetch revenue by industry."""
    query = f"""
    SELECT 
        INDUSTRY,
        COUNT(DISTINCT CUSTOMER_ID) as CUSTOMER_COUNT,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as ORDER_COUNT
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY INDUSTRY
    ORDER BY TOTAL_REVENUE DESC
    LIMIT 10
    """
    return _conn.query(query)

# Load data with error handling and loading state
data_loaded = False
segment_data = pd.DataFrame()
top_customers = pd.DataFrame()
industry_data = pd.DataFrame()

with st.spinner("Loading customer data..."):
    try:
        segment_data = get_segment_summary(conn, date_start, date_end)
        top_customers = get_top_customers(conn, date_start, date_end)
        industry_data = get_industry_breakdown(conn, date_start, date_end)
        data_loaded = True
    except Exception as e:
        st.error(f"Failed to load customer data: {str(e)}")

# Segment overview
st.subheader("Customer Segments")

if data_loaded and len(segment_data) > 0:
    cols = st.columns(len(segment_data))
    for i, row in segment_data.iterrows():
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{row['SEGMENT']}**")
                st.metric("Revenue", f"${row['TOTAL_REVENUE']:,.0f}")
                st.metric("Customers", f"{row['CUSTOMER_COUNT']:,}")
                st.metric("Orders", f"{row['ORDER_COUNT']:,}")

    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**Revenue by Segment**")
            st.bar_chart(segment_data, x="SEGMENT", y="TOTAL_REVENUE", height=300)
    
    with col2:
        with st.container(border=True):
            st.markdown("**Top Industries**")
            if len(industry_data) > 0:
                st.bar_chart(industry_data.head(10), x="INDUSTRY", y="TOTAL_REVENUE", height=300, horizontal=True)

    # Top customers table
    st.subheader("Top Customers")
    if len(top_customers) > 0:
        # Segment filter
        segments = top_customers['SEGMENT'].unique().tolist()
        selected_segment = st.selectbox("Filter by Segment", ["All Segments"] + segments)
        
        if selected_segment != "All Segments":
            filtered_customers = top_customers[top_customers['SEGMENT'] == selected_segment]
        else:
            filtered_customers = top_customers
        
        with st.container(border=True):
            st.dataframe(
                filtered_customers,
                hide_index=True,
                column_config={
                    "CUSTOMER_NAME": "Customer",
                    "SEGMENT": "Segment",
                    "TOTAL_REVENUE": st.column_config.NumberColumn("Total Revenue", format="$%.0f"),
                    "ORDER_COUNT": st.column_config.NumberColumn("Orders", format="%d"),
                    "AVG_ORDER_VALUE": st.column_config.NumberColumn("AOV", format="$%.2f"),
                    "FIRST_ORDER_DATE": st.column_config.DateColumn("First Order"),
                    "LAST_ORDER_DATE": st.column_config.DateColumn("Last Order"),
                },
                use_container_width=True,
                height=400
            )
elif data_loaded:
    st.info("No customer data available for selected period")
