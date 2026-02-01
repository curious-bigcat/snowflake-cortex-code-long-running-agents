-- ============================================================================
-- SALES ANALYTICS PLATFORM - SNOWFLAKE SETUP SCRIPT
-- ============================================================================
-- This script creates all Snowflake objects for the Sales Analytics Platform.
-- Run sections in order. Estimated time: 5-10 minutes.
-- ============================================================================

-- ============================================================================
-- PHASE 1: INFRASTRUCTURE
-- ============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS SALES_ANALYTICS_DB;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS SALES_ANALYTICS_DB.RAW;
CREATE SCHEMA IF NOT EXISTS SALES_ANALYTICS_DB.STAGING;
CREATE SCHEMA IF NOT EXISTS SALES_ANALYTICS_DB.MARTS;
CREATE SCHEMA IF NOT EXISTS SALES_ANALYTICS_DB.SEMANTIC;

-- Create warehouse
CREATE WAREHOUSE IF NOT EXISTS SALES_ANALYTICS_WH
    WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 120
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

-- Set context
USE DATABASE SALES_ANALYTICS_DB;
USE WAREHOUSE SALES_ANALYTICS_WH;

-- ============================================================================
-- PHASE 2: RAW DATA TABLES
-- ============================================================================

-- Customers table (10,000 rows)
CREATE OR REPLACE TABLE RAW.CUSTOMERS (
    CUSTOMER_ID NUMBER PRIMARY KEY,
    CUSTOMER_NAME VARCHAR(100),
    SEGMENT VARCHAR(20),        -- Enterprise (10%), SMB (30%), Consumer (60%)
    INDUSTRY VARCHAR(50),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Products table (500 rows)
CREATE OR REPLACE TABLE RAW.PRODUCTS (
    PRODUCT_ID NUMBER PRIMARY KEY,
    PRODUCT_NAME VARCHAR(100),
    CATEGORY VARCHAR(50),       -- 10 categories
    SUBCATEGORY VARCHAR(50),
    LIST_PRICE NUMBER(10,2)     -- $10 - $5,000
);

-- Sales Reps table (50 rows)
CREATE OR REPLACE TABLE RAW.SALES_REPS (
    SALES_REP_ID NUMBER PRIMARY KEY,
    REP_NAME VARCHAR(100),
    TEAM VARCHAR(50),
    REGION VARCHAR(20),         -- North, South, East, West
    HIRE_DATE DATE
);

-- Orders table (100,000 rows)
CREATE OR REPLACE TABLE RAW.ORDERS (
    ORDER_ID NUMBER PRIMARY KEY,
    CUSTOMER_ID NUMBER,
    PRODUCT_ID NUMBER,
    SALES_REP_ID NUMBER,
    ORDER_DATE DATE,
    QUANTITY NUMBER,
    UNIT_PRICE NUMBER(10,2),
    DISCOUNT_PCT NUMBER(5,4),   -- 0-0.25 (0-25%)
    REGION VARCHAR(20)
);

-- ============================================================================
-- PHASE 2: POPULATE RAW DATA WITH SAMPLE DATA
-- ============================================================================

-- Generate Customers (10,000 rows)
INSERT INTO RAW.CUSTOMERS (CUSTOMER_ID, CUSTOMER_NAME, SEGMENT, INDUSTRY, CREATED_AT)
SELECT 
    SEQ4() + 1 as CUSTOMER_ID,
    'Customer_' || LPAD(SEQ4() + 1, 5, '0') as CUSTOMER_NAME,
    CASE 
        WHEN RANDOM() < 0.1 THEN 'Enterprise'
        WHEN RANDOM() < 0.4 THEN 'SMB'
        ELSE 'Consumer'
    END as SEGMENT,
    ARRAY_CONSTRUCT('Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 
                    'Education', 'Government', 'Media', 'Energy', 'Transportation')
        [ABS(MOD(RANDOM(), 10))]::VARCHAR as INDUSTRY,
    DATEADD('day', -ABS(MOD(RANDOM(), 1095)), CURRENT_DATE()) as CREATED_AT
FROM TABLE(GENERATOR(ROWCOUNT => 10000));

-- Generate Products (500 rows)
INSERT INTO RAW.PRODUCTS (PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUBCATEGORY, LIST_PRICE)
SELECT 
    SEQ4() + 1 as PRODUCT_ID,
    'Product_' || LPAD(SEQ4() + 1, 4, '0') as PRODUCT_NAME,
    ARRAY_CONSTRUCT('ELECTRONICS', 'CLOTHING', 'HOME', 'SPORTS', 'BOOKS', 
                    'TOYS', 'BEAUTY', 'FOOD', 'AUTOMOTIVE', 'OFFICE')
        [ABS(MOD(RANDOM(), 10))]::VARCHAR as CATEGORY,
    'Subcategory_' || ABS(MOD(RANDOM(), 5) + 1) as SUBCATEGORY,
    ROUND(10 + (RANDOM() / 9223372036854775807::FLOAT + 0.5) * 4990, 2) as LIST_PRICE
FROM TABLE(GENERATOR(ROWCOUNT => 500));

-- Generate Sales Reps (50 rows)
INSERT INTO RAW.SALES_REPS (SALES_REP_ID, REP_NAME, TEAM, REGION, HIRE_DATE)
SELECT 
    SEQ4() + 1 as SALES_REP_ID,
    'Rep_' || LPAD(SEQ4() + 1, 3, '0') as REP_NAME,
    'Team_' || (MOD(SEQ4(), 5) + 1) as TEAM,
    ARRAY_CONSTRUCT('North', 'South', 'East', 'West')
        [MOD(SEQ4(), 4)]::VARCHAR as REGION,
    DATEADD('day', -ABS(MOD(RANDOM(), 1825)), CURRENT_DATE()) as HIRE_DATE
FROM TABLE(GENERATOR(ROWCOUNT => 50));

-- Generate Orders (100,000 rows with seasonal patterns)
INSERT INTO RAW.ORDERS (ORDER_ID, CUSTOMER_ID, PRODUCT_ID, SALES_REP_ID, ORDER_DATE, QUANTITY, UNIT_PRICE, DISCOUNT_PCT, REGION)
SELECT 
    SEQ4() + 1 as ORDER_ID,
    ABS(MOD(RANDOM(), 10000)) + 1 as CUSTOMER_ID,
    ABS(MOD(RANDOM(), 500)) + 1 as PRODUCT_ID,
    ABS(MOD(RANDOM(), 50)) + 1 as SALES_REP_ID,
    DATEADD('day', -ABS(MOD(RANDOM(), 730)), CURRENT_DATE()) as ORDER_DATE,
    ABS(MOD(RANDOM(), 10)) + 1 as QUANTITY,
    ROUND(10 + (RANDOM() / 9223372036854775807::FLOAT + 0.5) * 990, 2) as UNIT_PRICE,
    CASE WHEN RANDOM() < 0.1 THEN ROUND((RANDOM() / 9223372036854775807::FLOAT + 0.5) * 0.25, 4) ELSE 0 END as DISCOUNT_PCT,
    ARRAY_CONSTRUCT('North', 'South', 'East', 'West')
        [ABS(MOD(RANDOM(), 4))]::VARCHAR as REGION
FROM TABLE(GENERATOR(ROWCOUNT => 100000));

-- ============================================================================
-- PHASE 3: STAGING VIEWS
-- ============================================================================

-- Staging view for Customers
CREATE OR REPLACE VIEW STAGING.STG_CUSTOMERS AS
SELECT 
    CUSTOMER_ID,
    CUSTOMER_NAME,
    SEGMENT,
    INDUSTRY,
    CREATED_AT,
    -- Data quality flag
    CASE 
        WHEN CUSTOMER_ID IS NULL OR CUSTOMER_NAME IS NULL OR SEGMENT IS NULL THEN FALSE
        ELSE TRUE 
    END AS IS_VALID
FROM RAW.CUSTOMERS;

-- Staging view for Products
CREATE OR REPLACE VIEW STAGING.STG_PRODUCTS AS
SELECT 
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    SUBCATEGORY,
    LIST_PRICE,
    -- Data quality flag
    CASE 
        WHEN PRODUCT_ID IS NULL OR PRODUCT_NAME IS NULL OR CATEGORY IS NULL OR LIST_PRICE <= 0 THEN FALSE
        ELSE TRUE 
    END AS IS_VALID
FROM RAW.PRODUCTS;

-- Staging view for Sales Reps
CREATE OR REPLACE VIEW STAGING.STG_SALES_REPS AS
SELECT 
    SALES_REP_ID,
    REP_NAME,
    TEAM,
    REGION,
    HIRE_DATE,
    -- Data quality flag
    CASE 
        WHEN SALES_REP_ID IS NULL OR REP_NAME IS NULL OR REGION IS NULL THEN FALSE
        ELSE TRUE 
    END AS IS_VALID
FROM RAW.SALES_REPS;

-- Staging view for Orders
CREATE OR REPLACE VIEW STAGING.STG_ORDERS AS
SELECT 
    ORDER_ID,
    CUSTOMER_ID,
    PRODUCT_ID,
    SALES_REP_ID,
    ORDER_DATE,
    QUANTITY,
    UNIT_PRICE,
    DISCOUNT_PCT,
    REGION AS ORDER_REGION,
    -- Calculated fields
    QUANTITY * UNIT_PRICE AS GROSS_AMOUNT,
    QUANTITY * UNIT_PRICE * (1 - COALESCE(DISCOUNT_PCT, 0)) AS NET_AMOUNT,
    QUANTITY * UNIT_PRICE * COALESCE(DISCOUNT_PCT, 0) AS DISCOUNT_AMOUNT,
    -- Date parts
    DATE_TRUNC('week', ORDER_DATE) AS ORDER_WEEK,
    DATE_TRUNC('month', ORDER_DATE) AS ORDER_MONTH,
    DATE_TRUNC('quarter', ORDER_DATE) AS ORDER_QUARTER,
    YEAR(ORDER_DATE) AS ORDER_YEAR,
    -- Data quality flag
    CASE 
        WHEN ORDER_ID IS NULL OR CUSTOMER_ID IS NULL OR PRODUCT_ID IS NULL 
             OR ORDER_DATE IS NULL OR QUANTITY <= 0 OR UNIT_PRICE <= 0 THEN FALSE
        ELSE TRUE 
    END AS IS_VALID
FROM RAW.ORDERS;

-- ============================================================================
-- PHASE 4: MARTS - FACT TABLE (Dynamic Table)
-- ============================================================================

-- FCT_ORDERS: Main fact table joining all dimensions
CREATE OR REPLACE DYNAMIC TABLE MARTS.FCT_ORDERS
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    -- Order keys
    o.ORDER_ID,
    o.ORDER_DATE,
    o.ORDER_WEEK,
    o.ORDER_MONTH,
    o.ORDER_QUARTER,
    o.ORDER_YEAR,
    
    -- Customer dimension
    o.CUSTOMER_ID,
    c.CUSTOMER_NAME,
    c.SEGMENT AS CUSTOMER_SEGMENT,
    c.INDUSTRY,
    
    -- Product dimension
    o.PRODUCT_ID,
    p.PRODUCT_NAME,
    p.CATEGORY,
    p.SUBCATEGORY,
    p.LIST_PRICE,
    
    -- Sales rep dimension
    o.SALES_REP_ID,
    r.REP_NAME,
    r.TEAM,
    r.REGION AS REP_REGION,
    
    -- Order details
    o.ORDER_REGION,
    o.QUANTITY,
    o.UNIT_PRICE,
    o.DISCOUNT_PCT,
    
    -- Calculated amounts
    o.GROSS_AMOUNT,
    o.NET_AMOUNT,
    o.DISCOUNT_AMOUNT
    
FROM STAGING.STG_ORDERS o
LEFT JOIN STAGING.STG_CUSTOMERS c ON o.CUSTOMER_ID = c.CUSTOMER_ID
LEFT JOIN STAGING.STG_PRODUCTS p ON o.PRODUCT_ID = p.PRODUCT_ID
LEFT JOIN STAGING.STG_SALES_REPS r ON o.SALES_REP_ID = r.SALES_REP_ID
WHERE o.IS_VALID = TRUE;

-- ============================================================================
-- PHASE 5: MARTS - AGGREGATION DYNAMIC TABLES
-- ============================================================================

-- DAILY_SALES: Daily aggregation
CREATE OR REPLACE DYNAMIC TABLE MARTS.DAILY_SALES
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    ORDER_DATE,
    SUM(NET_AMOUNT) AS REVENUE,
    SUM(GROSS_AMOUNT) AS GROSS_REVENUE,
    SUM(DISCOUNT_AMOUNT) AS DISCOUNT_TOTAL,
    COUNT(*) AS ORDER_COUNT,
    COUNT(DISTINCT CUSTOMER_ID) AS CUSTOMER_COUNT,
    SUM(QUANTITY) AS UNITS_SOLD,
    AVG(NET_AMOUNT) AS AVG_ORDER_VALUE
FROM MARTS.FCT_ORDERS
GROUP BY ORDER_DATE;

-- SALES_BY_REGION: Regional aggregation by month
CREATE OR REPLACE DYNAMIC TABLE MARTS.SALES_BY_REGION
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    ORDER_REGION AS REGION,
    ORDER_MONTH,
    SUM(NET_AMOUNT) AS REVENUE,
    COUNT(*) AS ORDER_COUNT,
    COUNT(DISTINCT CUSTOMER_ID) AS CUSTOMER_COUNT,
    AVG(NET_AMOUNT) AS AVG_ORDER_VALUE
FROM MARTS.FCT_ORDERS
GROUP BY ORDER_REGION, ORDER_MONTH;

-- SALES_BY_PRODUCT: Product aggregation by month
CREATE OR REPLACE DYNAMIC TABLE MARTS.SALES_BY_PRODUCT
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    PRODUCT_ID,
    PRODUCT_NAME,
    CATEGORY,
    SUBCATEGORY,
    ORDER_MONTH AS MONTH,
    SUM(NET_AMOUNT) AS REVENUE,
    COUNT(*) AS ORDER_COUNT,
    SUM(QUANTITY) AS UNITS_SOLD,
    AVG(NET_AMOUNT) AS AVG_ORDER_VALUE
FROM MARTS.FCT_ORDERS
GROUP BY PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUBCATEGORY, ORDER_MONTH;

-- SALES_BY_CUSTOMER: Customer aggregation
CREATE OR REPLACE DYNAMIC TABLE MARTS.SALES_BY_CUSTOMER
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    CUSTOMER_ID,
    CUSTOMER_NAME,
    CUSTOMER_SEGMENT,
    INDUSTRY,
    SUM(NET_AMOUNT) AS TOTAL_REVENUE,
    COUNT(*) AS ORDER_COUNT,
    AVG(NET_AMOUNT) AS AVG_ORDER_VALUE,
    MIN(ORDER_DATE) AS FIRST_ORDER_DATE,
    MAX(ORDER_DATE) AS LAST_ORDER_DATE
FROM MARTS.FCT_ORDERS
GROUP BY CUSTOMER_ID, CUSTOMER_NAME, CUSTOMER_SEGMENT, INDUSTRY;

-- SALES_BY_REP: Sales rep aggregation by month
CREATE OR REPLACE DYNAMIC TABLE MARTS.SALES_BY_REP
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    SALES_REP_ID,
    REP_NAME,
    TEAM,
    REP_REGION AS REGION,
    ORDER_MONTH AS MONTH,
    SUM(NET_AMOUNT) AS REVENUE,
    COUNT(*) AS ORDER_COUNT,
    COUNT(DISTINCT CUSTOMER_ID) AS CUSTOMER_COUNT,
    AVG(NET_AMOUNT) AS AVG_ORDER_VALUE
FROM MARTS.FCT_ORDERS
GROUP BY SALES_REP_ID, REP_NAME, TEAM, REP_REGION, ORDER_MONTH;

-- ============================================================================
-- PHASE 6: SEMANTIC MODEL STAGE
-- ============================================================================

-- Create stage for semantic model YAML files
CREATE OR REPLACE STAGE SEMANTIC.SEMANTIC_MODELS
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage for Cortex Analyst semantic model files';

-- Note: Upload sales_model.yaml to this stage using:
-- PUT file://path/to/sales_model.yaml @SEMANTIC.SEMANTIC_MODELS AUTO_COMPRESS=FALSE;

-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Check row counts
SELECT 'RAW.CUSTOMERS' as TABLE_NAME, COUNT(*) as ROW_COUNT FROM RAW.CUSTOMERS
UNION ALL SELECT 'RAW.PRODUCTS', COUNT(*) FROM RAW.PRODUCTS
UNION ALL SELECT 'RAW.SALES_REPS', COUNT(*) FROM RAW.SALES_REPS
UNION ALL SELECT 'RAW.ORDERS', COUNT(*) FROM RAW.ORDERS
UNION ALL SELECT 'MARTS.FCT_ORDERS', COUNT(*) FROM MARTS.FCT_ORDERS
UNION ALL SELECT 'MARTS.DAILY_SALES', COUNT(*) FROM MARTS.DAILY_SALES
UNION ALL SELECT 'MARTS.SALES_BY_REGION', COUNT(*) FROM MARTS.SALES_BY_REGION
UNION ALL SELECT 'MARTS.SALES_BY_PRODUCT', COUNT(*) FROM MARTS.SALES_BY_PRODUCT
UNION ALL SELECT 'MARTS.SALES_BY_CUSTOMER', COUNT(*) FROM MARTS.SALES_BY_CUSTOMER
UNION ALL SELECT 'MARTS.SALES_BY_REP', COUNT(*) FROM MARTS.SALES_BY_REP;

-- Check Dynamic Table status
SHOW DYNAMIC TABLES IN SCHEMA MARTS;

-- Verify total revenue (should be ~$394M)
SELECT 
    SUM(NET_AMOUNT) as TOTAL_REVENUE,
    COUNT(*) as ORDER_COUNT,
    COUNT(DISTINCT CUSTOMER_ID) as CUSTOMER_COUNT
FROM MARTS.FCT_ORDERS;

-- ============================================================================
-- CLEANUP (if needed)
-- ============================================================================
-- DROP DATABASE SALES_ANALYTICS_DB;
-- DROP WAREHOUSE SALES_ANALYTICS_WH;
