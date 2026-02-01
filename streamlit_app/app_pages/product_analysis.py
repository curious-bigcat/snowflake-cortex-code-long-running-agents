"""
Product Analysis - Sales performance by product and category
"""
import streamlit as st
from datetime import timedelta
import pandas as pd

conn = st.session_state.conn
date_start = st.session_state.date_start
date_end = st.session_state.date_end

st.title(":material/inventory_2: Product Analysis")

@st.cache_data(ttl=timedelta(minutes=5))
def get_category_summary(_conn, start_date, end_date):
    """Fetch category-level summary."""
    query = f"""
    SELECT 
        CATEGORY,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as TOTAL_ORDERS,
        SUM(QUANTITY) as TOTAL_UNITS
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY CATEGORY
    ORDER BY TOTAL_REVENUE DESC
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_top_products(_conn, start_date, end_date, limit=20):
    """Fetch top products by revenue."""
    query = f"""
    SELECT 
        PRODUCT_NAME,
        CATEGORY,
        SUM(NET_AMOUNT) as TOTAL_REVENUE,
        COUNT(*) as TOTAL_ORDERS,
        SUM(QUANTITY) as TOTAL_UNITS
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY PRODUCT_NAME, CATEGORY
    ORDER BY TOTAL_REVENUE DESC
    LIMIT {limit}
    """
    return _conn.query(query)

@st.cache_data(ttl=timedelta(minutes=5))
def get_category_trend(_conn, start_date, end_date):
    """Fetch monthly trend by category."""
    query = f"""
    SELECT 
        DATE_TRUNC('month', ORDER_DATE) as MONTH,
        CATEGORY,
        SUM(NET_AMOUNT) as REVENUE
    FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS
    WHERE ORDER_DATE BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY DATE_TRUNC('month', ORDER_DATE), CATEGORY
    ORDER BY MONTH, CATEGORY
    """
    return _conn.query(query)

# Load data with error handling and loading state
data_loaded = False
category_summary = pd.DataFrame()
top_products = pd.DataFrame()
category_trend = pd.DataFrame()

with st.spinner("Loading product data..."):
    try:
        category_summary = get_category_summary(conn, date_start, date_end)
        top_products = get_top_products(conn, date_start, date_end)
        category_trend = get_category_trend(conn, date_start, date_end)
        data_loaded = True
    except Exception as e:
        st.error(f"Failed to load product data: {str(e)}")

# Category filter
if data_loaded and len(category_summary) > 0:
    categories = category_summary['CATEGORY'].tolist()
    selected_categories = st.multiselect(
        "Filter by Category",
        options=categories,
        default=categories[:5] if len(categories) > 5 else categories
    )
    
    # Category KPIs
    st.subheader("Category Performance")
    filtered_cats = category_summary[category_summary['CATEGORY'].isin(selected_categories)]
    
    with st.container(border=True):
        st.bar_chart(filtered_cats, x="CATEGORY", y="TOTAL_REVENUE", height=300)
    
    # Category metrics
    cols = st.columns(min(4, len(selected_categories)))
    for i, cat in enumerate(selected_categories[:4]):
        cat_row = filtered_cats[filtered_cats['CATEGORY'] == cat]
        if len(cat_row) > 0:
            with cols[i]:
                rev = cat_row['TOTAL_REVENUE'].iloc[0]
                units = cat_row['TOTAL_UNITS'].iloc[0]
                st.metric(cat, f"${rev:,.0f}", f"{units:,} units")
    
    # Trend chart
    st.subheader("Category Trends")
    with st.container(border=True):
        trend_filtered = category_trend[category_trend['CATEGORY'].isin(selected_categories)]
        if len(trend_filtered) > 0:
            pivot = trend_filtered.pivot(index='MONTH', columns='CATEGORY', values='REVENUE')
            st.line_chart(pivot, height=350)
    
    # Top products table
    st.subheader("Top Products")
    with st.container(border=True):
        products_filtered = top_products[top_products['CATEGORY'].isin(selected_categories)]
        st.dataframe(
            products_filtered,
            hide_index=True,
            column_config={
                "PRODUCT_NAME": "Product",
                "CATEGORY": "Category",
                "TOTAL_REVENUE": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                "TOTAL_ORDERS": st.column_config.NumberColumn("Orders", format="%d"),
                "TOTAL_UNITS": st.column_config.NumberColumn("Units", format="%d"),
            },
            use_container_width=True
        )
    
    # Drill-down by category
    st.subheader("Category Drill-Down")
    selected_drill_cat = st.selectbox(
        "Select category to drill down",
        options=selected_categories,
        key="drill_category"
    )
    
    if selected_drill_cat:
        with st.expander(f"Details for {selected_drill_cat}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Category stats
                cat_stats = filtered_cats[filtered_cats['CATEGORY'] == selected_drill_cat]
                if len(cat_stats) > 0:
                    total_rev = filtered_cats['TOTAL_REVENUE'].sum()
                    cat_rev = cat_stats['TOTAL_REVENUE'].iloc[0]
                    pct = (cat_rev / total_rev * 100) if total_rev > 0 else 0
                    
                    st.metric("Category Revenue", f"${cat_rev:,.0f}")
                    st.metric("% of Selected Categories", f"{pct:.1f}%")
                    st.metric("Total Orders", f"{cat_stats['TOTAL_ORDERS'].iloc[0]:,}")
                    st.metric("Units Sold", f"{cat_stats['TOTAL_UNITS'].iloc[0]:,}")
            
            with col2:
                # Monthly trend for this category
                cat_trend = category_trend[category_trend['CATEGORY'] == selected_drill_cat]
                if len(cat_trend) > 0:
                    st.markdown("**Monthly Revenue Trend**")
                    st.line_chart(cat_trend, x="MONTH", y="REVENUE", height=200)
            
            # Products in this category
            st.markdown("**Products in Category**")
            cat_products = top_products[top_products['CATEGORY'] == selected_drill_cat]
            if len(cat_products) > 0:
                st.dataframe(
                    cat_products,
                    hide_index=True,
                    column_config={
                        "PRODUCT_NAME": "Product",
                        "CATEGORY": None,  # Hide category column
                        "TOTAL_REVENUE": st.column_config.NumberColumn("Revenue", format="$%.0f"),
                        "TOTAL_ORDERS": st.column_config.NumberColumn("Orders", format="%d"),
                        "TOTAL_UNITS": st.column_config.NumberColumn("Units", format="%d"),
                    },
                    use_container_width=True,
                    height=250
                )
            else:
                st.info("No products in top 20 for this category")
elif data_loaded:
    st.info("No product data available for selected period")
