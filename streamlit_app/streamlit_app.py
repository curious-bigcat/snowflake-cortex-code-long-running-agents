"""
Sales Analytics Platform - Main Streamlit Application
Built on Snowflake Dynamic Tables with Cortex Analyst integration
"""
import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Platform",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Snowflake connection with retry logic
@st.cache_resource
def get_connection():
    """Get cached Snowflake connection with error handling."""
    try:
        conn = st.connection("snowflake")
        # Test connection with simple query
        conn.query("SELECT 1")
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

# Initialize global session state
if "conn" not in st.session_state:
    st.session_state.conn = get_connection()

# Check connection health
if st.session_state.conn is None:
    st.error("Unable to establish Snowflake connection. Please check your configuration.")
    st.stop()

# Default date range (last 12 months)
if "date_start" not in st.session_state:
    st.session_state.date_start = datetime.now().date() - timedelta(days=365)
if "date_end" not in st.session_state:
    st.session_state.date_end = datetime.now().date()

# Define navigation pages
pages = {
    "": [
        st.Page("app_pages/executive_dashboard.py", title="Executive Dashboard", icon=":material/dashboard:"),
    ],
    "Analysis": [
        st.Page("app_pages/regional_analysis.py", title="Regional Analysis", icon=":material/map:"),
        st.Page("app_pages/product_analysis.py", title="Product Analysis", icon=":material/inventory_2:"),
        st.Page("app_pages/sales_rep_leaderboard.py", title="Sales Rep Leaderboard", icon=":material/leaderboard:"),
        st.Page("app_pages/customer_insights.py", title="Customer Insights", icon=":material/groups:"),
    ],
    "AI": [
        st.Page("app_pages/cortex_analyst.py", title="Ask Cortex", icon=":material/smart_toy:"),
    ],
}

# Create navigation
page = st.navigation(pages, position="sidebar")

# Sidebar - Global filters
with st.sidebar:
    st.markdown("---")
    st.subheader(":material/filter_alt: Filters")
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        date_start = st.date_input(
            "Start Date",
            value=st.session_state.date_start,
            key="filter_date_start"
        )
    with col2:
        date_end = st.date_input(
            "End Date", 
            value=st.session_state.date_end,
            key="filter_date_end"
        )
    
    # Validate date range
    if date_start > date_end:
        st.warning("Start date must be before end date")
        date_start = date_end - timedelta(days=30)
    
    # Update session state
    st.session_state.date_start = date_start
    st.session_state.date_end = date_end
    
    # Quick date presets
    st.markdown("**Quick Select:**")
    preset_cols = st.columns(3)
    with preset_cols[0]:
        if st.button("30D", use_container_width=True):
            st.session_state.date_start = datetime.now().date() - timedelta(days=30)
            st.session_state.date_end = datetime.now().date()
            st.rerun()
    with preset_cols[1]:
        if st.button("90D", use_container_width=True):
            st.session_state.date_start = datetime.now().date() - timedelta(days=90)
            st.session_state.date_end = datetime.now().date()
            st.rerun()
    with preset_cols[2]:
        if st.button("1Y", use_container_width=True):
            st.session_state.date_start = datetime.now().date() - timedelta(days=365)
            st.session_state.date_end = datetime.now().date()
            st.rerun()
    
    st.markdown("---")
    
    # Cache control
    if st.button("Refresh Data", use_container_width=True, type="secondary"):
        st.cache_data.clear()
        st.rerun()
    
    st.caption("Data refreshes every 5 minutes via Dynamic Tables")
    
    # About section with documentation
    st.markdown("---")
    with st.expander("About This Platform", expanded=False):
        st.markdown("""
        **Sales Analytics Platform**
        
        A real-time analytics dashboard built on Snowflake Dynamic Tables.
        
        **Pages:**
        - **Executive Dashboard**: KPIs, revenue trends, regional overview
        - **Regional Analysis**: Geographic performance breakdown
        - **Product Analysis**: Category and product metrics
        - **Sales Rep Leaderboard**: Rep performance rankings
        - **Customer Insights**: Segment analysis
        - **Ask Cortex**: AI-powered natural language queries
        
        **Data:**
        - Source: SALES_ANALYTICS_DB
        - Refresh: 5-minute target lag
        - Date range: 2024-02 to present
        
        **Tips:**
        - Use date filters to focus analysis
        - Expand drill-down sections for details
        - Click "Refresh Data" for latest updates
        """)

# Run the selected page
page.run()
