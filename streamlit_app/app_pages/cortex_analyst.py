"""
Cortex Analyst - Natural language queries powered by AI
"""
import streamlit as st
from datetime import timedelta

conn = st.session_state.conn

st.title(":material/smart_toy: Ask Cortex")
st.markdown("Ask questions about your sales data in natural language.")

# Initialize chat history
if "analyst_messages" not in st.session_state:
    st.session_state.analyst_messages = []

# Semantic model path
SEMANTIC_MODEL = "@SALES_ANALYTICS_DB.SEMANTIC.SEMANTIC_MODELS/sales_model.yaml"

# Example questions
with st.expander("Example Questions", expanded=False):
    st.markdown("""
    Try asking questions like:
    - What was total revenue last month?
    - Show me the top 10 products by revenue
    - Which region has the highest sales?
    - What is the average order value by customer segment?
    - How many orders did we have in Q4 2025?
    - Who are our top 5 customers?
    - Show me monthly revenue trend for 2025
    """)

# Display chat history
for message in st.session_state.analyst_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sql" in message:
            with st.expander("View SQL"):
                st.code(message["sql"], language="sql")
        if "data" in message:
            st.dataframe(message["data"], hide_index=True)

# Chat input
if prompt := st.chat_input("Ask a question about your sales data..."):
    # Add user message
    st.session_state.analyst_messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                # Call Cortex Analyst
                response = conn.query(f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        'mistral-large2',
                        'You are a SQL expert. Given this question about sales data, generate a Snowflake SQL query.
                        
The data is in SALES_ANALYTICS_DB.MARTS.FCT_ORDERS with columns:
- ORDER_ID, ORDER_DATE, CUSTOMER_ID, CUSTOMER_NAME, CUSTOMER_SEGMENT, INDUSTRY
- PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUBCATEGORY
- SALES_REP_ID, REP_NAME, REGION (as ORDER_REGION)
- QUANTITY, UNIT_PRICE, DISCOUNT_PCT, GROSS_AMOUNT, NET_AMOUNT, DISCOUNT_AMOUNT
- ORDER_WEEK, ORDER_MONTH, ORDER_QUARTER, ORDER_YEAR

For revenue, use NET_AMOUNT (after discounts).
Return ONLY the SQL query, no explanation.

Question: {prompt}'
                    ) as SQL_QUERY
                """)
                
                # Extract and clean SQL
                sql_query = response['SQL_QUERY'].iloc[0].strip()
                sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
                
                # Execute the query
                result_df = conn.query(sql_query)
                
                # Format response
                response_text = f"Here are the results for: *{prompt}*"
                st.markdown(response_text)
                
                with st.expander("View SQL", expanded=False):
                    st.code(sql_query, language="sql")
                
                st.dataframe(result_df, hide_index=True, use_container_width=True)
                
                # Save to history
                st.session_state.analyst_messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "sql": sql_query,
                    "data": result_df
                })
                
            except Exception as e:
                error_msg = f"Sorry, I couldn't process that question. Error: {str(e)}"
                st.error(error_msg)
                st.session_state.analyst_messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Clear chat button
if st.session_state.analyst_messages:
    if st.button("Clear Chat", type="secondary"):
        st.session_state.analyst_messages = []
        st.rerun()
