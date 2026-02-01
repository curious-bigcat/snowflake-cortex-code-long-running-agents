"""
Executive Dashboard - KPIs and high-level metrics
"""
import streamlit as st
from datetime import timedelta
import pandas as pd

# Get connection and date filters from session state
conn = st.session_state.conn
date_start = st.session_state.date_start
date_end = st.session_state.date_end

st.title(":material/dashboard: Executive Dashboard")

# Fetch KPI data
@st.cache_data(ttl=timedelta(minutes=5))
def get_kpis(_conn, start_date, end_date):
    """Fetch KPI metrics for the date range."""
    query = f"""
    SELECT 
        SUM(NET_AMOUNT) as total_revenue,
        SUM(GROSS_AMOUNT) as gross_revenue,
        SUM(DISCOUNT_AMOUNT) as total_discounts,
        COUNT(*) as order_count,
        COUNT(DISTINCT CUSTOMER_ID) as customer_count,
        SUM(QUANTITY) as units_sold,
        AVG(NET_AMOUNT) as avg_order_value
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_daily_trend(_conn, start_date, end_date):
    """Fetch daily revenue trend."""
    query = f"""
    SELECT 
        ORDER_DATE,
        SUM(REVENUE) as REVENUE,
        SUM(ORDER_COUNT) as ORDERS
    FROM SALES_ANALYTICS_DB.MARTS.DAILY_SALES
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY ORDER_DATE
    ORDER BY ORDER_DATE
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_region_breakdown(_conn, start_date, end_date):
    """Fetch revenue by region."""
    query = f"""
    SELECT 
        ORDER_REGION as REGION,
        SUM(NET_AMOUNT) as REVENUE,
        COUNT(*) as ORDERS
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY ORDER_REGION
    ORDER BY REVENUE DESC
    """
    return _conn.query(query)

# Load data with error handling and loading state
data_loaded = False
kpis = pd.DataFrame()
daily_trend = pd.DataFrame()
region_data = pd.DataFrame()

with st.spinner("Loading dashboard data..."):
    try:
        kpis = get_kpis(conn, date_start, date_end)
        daily_trend = get_daily_trend(conn, date_start, date_end)
        region_data = get_region_breakdown(conn, date_start, date_end)
        data_loaded = True
    except Exception as e:
        st.error(f"Failed to load dashboard data: {str(e)}")

# KPI Cards Row
if data_loaded:
    st.subheader("Key Metrics")
    with st.container(border=True):
        cols = st.columns(4)
        
        with cols[0]:
            revenue = kpis['TOTAL_REVENUE'].iloc[0] if len(kpis) > 0 else 0
            st.metric(
                "Total Revenue",
                f"${revenue:,.0f}",
                help="Net revenue after discounts"
            )
        
        with cols[1]:
            orders = kpis['ORDER_COUNT'].iloc[0] if len(kpis) > 0 else 0
            st.metric(
                "Total Orders",
                f"{orders:,}",
                help="Number of orders in period"
            )
        
        with cols[2]:
            customers = kpis['CUSTOMER_COUNT'].iloc[0] if len(kpis) > 0 else 0
            st.metric(
                "Unique Customers",
                f"{customers:,}",
                help="Distinct customers with orders"
            )
        
        with cols[3]:
            aov = kpis['AVG_ORDER_VALUE'].iloc[0] if len(kpis) > 0 else 0
            st.metric(
                "Avg Order Value",
                f"${aov:,.2f}",
                help="Average revenue per order"
            )

    # Charts Row
    st.subheader("Trends & Breakdown")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("**Revenue Trend**")
            if len(daily_trend) > 0:
                st.line_chart(daily_trend, x="ORDER_DATE", y="REVENUE", height=300)
            else:
                st.info("No data for selected period")

    with col2:
        with st.container(border=True):
            st.markdown("**Revenue by Region**")
            if len(region_data) > 0:
                st.bar_chart(region_data, x="REGION", y="REVENUE", height=300)
            else:
                st.info("No data for selected period")

    # Drill-down sections
    st.subheader("Drill-Down Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("Daily Revenue Detail", expanded=False):
            if len(daily_trend) > 0:
                st.dataframe(
                    daily_trend.sort_values('ORDER_DATE', ascending=False),
                    hide_index=True,
                    column_config={
                        "ORDER_DATE": st.column_config.DateColumn("Date"),
                        "REVENUE": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                        "ORDERS": st.column_config.NumberColumn("Orders", format="%d"),
                    },
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("No data available")
    
    with col2:
        with st.expander("Regional Breakdown Detail", expanded=False):
            if len(region_data) > 0:
                # Calculate percentage of total (convert to float for arithmetic)
                region_detail = region_data.copy()
                region_detail['REVENUE'] = region_detail['REVENUE'].astype(float)
                total_rev = region_detail['REVENUE'].sum()
                region_detail['PCT_OF_TOTAL'] = (region_detail['REVENUE'] / total_rev * 100).round(1)
                st.dataframe(
                    region_detail,
                    hide_index=True,
                    column_config={
                        "REGION": "Region",
                        "REVENUE": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                        "ORDERS": st.column_config.NumberColumn("Orders", format="%d"),
                        "PCT_OF_TOTAL": st.column_config.NumberColumn("% of Total", format="%.1f%%"),
                    },
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("No data available")

    # Summary stats
    st.subheader("Period Summary")
    with st.container(border=True):
        if len(kpis) > 0:
            gross = kpis['GROSS_REVENUE'].iloc[0] or 0
            discounts = kpis['TOTAL_DISCOUNTS'].iloc[0] or 0
            units = kpis['UNITS_SOLD'].iloc[0] or 0
            
            summary_cols = st.columns(3)
            with summary_cols[0]:
                st.metric("Gross Revenue", f"${gross:,.0f}")
            with summary_cols[1]:
                st.metric("Total Discounts", f"${discounts:,.0f}")
            with summary_cols[2]:
                st.metric("Units Sold", f"{units:,}")
