# Sales Analytics Platform - Long-Running Project Specification

## How to Execute This Project

This project uses the **Long-Running Agents Pattern** for complex, multi-session work. Follow these instructions:

### Starting the Project (First Session)

```bash
cd /path/to/project
cortex
```

Then enter plan mode and provide this file:
```
/plan
Read @sales_analytics_platform.md and execute this long-running project following the agent pattern defined in the document.
```

### Continuing the Project (Subsequent Sessions)

```bash
cortex --continue
```

Or start fresh and reference the progress:
```
/plan
Continue the sales analytics project. Read feature_list.json and cortex-progress.md to understand current state, then implement the next incomplete feature.
```

---

# PART 1: LONG-RUNNING AGENT PATTERN

## Overview

This project is too large for a single context window. You must work **incrementally** across multiple sessions using this pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION 1 (Initialization)                                      │
│  ► Analyze requirements                                          │
│  ► Generate comprehensive feature_list.json (50-80 features)     │
│  ► Create progress tracking file                                 │
│  ► Set up Snowflake infrastructure                               │
│  ► Implement 2-3 foundational features                           │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  SESSION 2+ (Incremental Progress)                               │
│  ► Read cortex-progress.md to understand recent work             │
│  ► Read feature_list.json to find next incomplete feature        │
│  ► Validate existing objects still work                          │
│  ► Implement ONE feature completely                              │
│  ► Test thoroughly                                               │
│  ► Update progress files                                         │
│  ► Leave clean state for next session                            │
└─────────────────────────────────────────────────────────────────┘
                              ▼
                    (Repeat until all features pass)
```

## Critical Rules

1. **ONE FEATURE AT A TIME** - Never try to implement multiple features in one session
2. **TEST EVERYTHING** - A feature is not done until verified with queries/tests
3. **DOCUMENT THOROUGHLY** - The next session has NO memory of your work
4. **NEVER BREAK EXISTING FEATURES** - Always validate before adding new
5. **LEAVE CLEAN STATE** - No half-implemented code or broken objects

## Required Artifacts

### 1. feature_list.json

Create this file in Session 1. Structure:

```json
{
  "project": "Sales Analytics Platform",
  "created": "2024-01-15T10:00:00Z",
  "features": [
    {
      "id": 1,
      "phase": "infrastructure",
      "priority": 1,
      "title": "Create database and schemas",
      "description": "Create SALES_ANALYTICS_DB with RAW, STAGING, MARTS schemas",
      "acceptance_criteria": [
        "Database exists",
        "All three schemas created",
        "Current role has access"
      ],
      "passes": false,
      "tested_at": null,
      "notes": ""
    }
  ]
}
```

**Rules for feature_list.json:**
- Generate 50-80 features covering ALL requirements below
- Order by dependency (infrastructure → ingestion → transformation → semantic → app)
- ONLY update `passes`, `tested_at`, `notes` fields - never delete or reorder features
- Mark `passes: true` ONLY after successful testing

### 2. cortex-progress.md

Create this file in Session 1. Structure:

```markdown
# Sales Analytics Platform - Progress Log

## Quick Status
- **Total Features**: X
- **Completed**: Y
- **Remaining**: Z
- **Last Updated**: <timestamp>

## Session History

### Session 1 - <date>
- **Type**: Initialization
- **Features Completed**: #1, #2, #3
- **Objects Created**: DATABASE, SCHEMAS, WAREHOUSE
- **Issues**: None
- **Next**: Implement feature #4 (Create raw tables)

---

## Current Snowflake Objects

| Type | Name | Schema | Status |
|------|------|--------|--------|
| DATABASE | SALES_ANALYTICS_DB | - | ✓ |
| SCHEMA | RAW | SALES_ANALYTICS_DB | ✓ |

## Known Issues / Blockers
(none)

## How to Validate Environment
\`\`\`sql
SHOW DATABASES LIKE 'SALES_ANALYTICS%';
SELECT COUNT(*) FROM SALES_ANALYTICS_DB.MARTS.DAILY_SALES;
\`\`\`
```

## Session Workflow

### Every Session Must:

1. **START** by reading `cortex-progress.md` and `feature_list.json`
2. **VALIDATE** existing objects with SQL queries
3. **SELECT** the next incomplete feature (lowest ID where `passes: false`)
4. **IMPLEMENT** that single feature completely
5. **TEST** with actual queries or app verification
6. **UPDATE** both progress files
7. **END** with clear notes for next session

### If You Run Out of Context:
1. Immediately update `cortex-progress.md` with current state
2. Document exactly where you stopped
3. The next session will continue from there

---

# PART 2: PROJECT REQUIREMENTS

## Business Context

**Goal**: Build a self-service sales analytics platform enabling sales leaders to track performance, identify trends, and make data-driven decisions without writing SQL.

**Users**: 
- Sales VPs (executive dashboards)
- Regional Managers (regional drill-downs)
- Sales Ops (detailed analysis via Cortex Analyst)

**Key Questions to Answer**:
- What was our revenue this month/quarter/year?
- How are we trending vs last period?
- Which regions/products/reps are over/under performing?
- What's our average deal size and how is it changing?

---

## Functional Requirements

### FR-1: Data Ingestion
- [ ] Ingest orders, customers, products, sales_reps data
- [ ] Support incremental updates (CDC pattern)
- [ ] Handle late-arriving data gracefully
- [ ] Data freshness: within 10 minutes of source

### FR-2: Data Transformation
- [ ] Calculate net revenue (quantity × price × (1 - discount))
- [ ] Aggregate to daily, weekly, monthly grains
- [ ] Join with dimension tables for enriched views
- [ ] Calculate period-over-period comparisons (WoW, MoM, YoY)
- [ ] Compute running totals and moving averages

### FR-3: Semantic Model (Cortex Analyst)
- [ ] Answer natural language questions about sales
- [ ] Support time intelligence ("last month", "vs prior year")
- [ ] Handle metric calculations (revenue, order count, AOV)
- [ ] Support dimensional slicing (by region, product, customer, rep)

**Required Test Questions** (must pass before semantic model is complete):
1. "What was total revenue last month?"
2. "Show top 10 customers by revenue this quarter"
3. "Compare revenue by region YoY"
4. "What's the average order value trend over the past 6 months?"
5. "Which sales rep has the highest revenue this year?"

### FR-4: Streamlit Dashboard
- [ ] Executive KPI summary (Revenue, Orders, AOV, Customers)
- [ ] Revenue trend chart (line chart, daily/weekly/monthly toggle)
- [ ] Regional performance comparison (bar chart)
- [ ] Product category breakdown (pie/donut chart)
- [ ] Sales rep leaderboard (table with rankings)
- [ ] Interactive filters: date range, region, segment, category
- [ ] Auto-refresh every 5 minutes

### FR-5: Data Quality
- [ ] No NULL values in key fields (order_id, amount, date)
- [ ] All amounts are positive
- [ ] Dates within valid range (not future, not before 2020)
- [ ] Referential integrity (all FKs exist in dimension tables)

---

## Technical Requirements

### TR-1: Snowflake Architecture

```
SALES_ANALYTICS_DB
├── RAW                    # Source data (tables)
│   ├── ORDERS
│   ├── CUSTOMERS  
│   ├── PRODUCTS
│   └── SALES_REPS
│
├── STAGING                # Cleaned data (views or tables)
│   ├── STG_ORDERS
│   ├── STG_CUSTOMERS
│   ├── STG_PRODUCTS
│   └── STG_SALES_REPS
│
├── MARTS                  # Aggregated data (Dynamic Tables)
│   ├── FCT_ORDERS         # Fact table with all dimensions joined
│   ├── DAILY_SALES        # Daily aggregation
│   ├── SALES_BY_REGION    # Regional rollup
│   ├── SALES_BY_PRODUCT   # Product rollup
│   ├── SALES_BY_CUSTOMER  # Customer rollup
│   └── SALES_BY_REP       # Rep rollup
│
└── SEMANTIC               # Semantic model files
    └── sales_model.yaml
```

### TR-2: Dynamic Tables Configuration
- Target lag: 5 minutes for mart tables
- Warehouse: SALES_ANALYTICS_WH (SMALL)
- Refresh mode: AUTO

### TR-3: Warehouse
- Name: SALES_ANALYTICS_WH
- Size: SMALL
- Auto-suspend: 120 seconds
- Auto-resume: TRUE

### TR-4: Sample Data Generation

Create realistic sample data:

**ORDERS** (100,000 rows):
```sql
-- Generate 2 years of order history
-- Columns: ORDER_ID, CUSTOMER_ID, PRODUCT_ID, SALES_REP_ID, 
--          ORDER_DATE, QUANTITY, UNIT_PRICE, DISCOUNT_PCT, REGION
-- Include seasonal patterns (Q4 spike, summer dip)
-- 10% of orders have discounts (5-25%)
```

**CUSTOMERS** (10,000 rows):
```sql
-- Columns: CUSTOMER_ID, CUSTOMER_NAME, SEGMENT, INDUSTRY, CREATED_AT
-- Segments: Enterprise (10%), SMB (30%), Consumer (60%)
```

**PRODUCTS** (500 rows):
```sql
-- Columns: PRODUCT_ID, PRODUCT_NAME, CATEGORY, SUBCATEGORY, LIST_PRICE
-- 10 categories, prices $10-$5,000
-- Follow 80/20 rule (20% products = 80% revenue)
```

**SALES_REPS** (50 rows):
```sql
-- Columns: SALES_REP_ID, REP_NAME, TEAM, REGION, HIRE_DATE
-- 4 regions: North, South, East, West
```

### TR-5: Semantic Model Schema

```yaml
name: sales_analytics
description: Sales performance analytics for revenue tracking and analysis

tables:
  - name: fct_orders
    description: Order-level fact table with all dimensions
    base_table:
      database: SALES_ANALYTICS_DB
      schema: MARTS
      table: FCT_ORDERS
    
    dimensions:
      - name: order_date
        expr: ORDER_DATE
        data_type: DATE
        description: Date the order was placed
        
      - name: region
        expr: REGION
        data_type: VARCHAR
        description: Sales region
        sample_values: ["North", "South", "East", "West"]
        
      - name: customer_segment
        expr: CUSTOMER_SEGMENT
        data_type: VARCHAR
        description: Customer segment
        sample_values: ["Enterprise", "SMB", "Consumer"]
        
      - name: product_category
        expr: PRODUCT_CATEGORY
        data_type: VARCHAR
        description: Product category
        
      - name: sales_rep_name
        expr: SALES_REP_NAME
        data_type: VARCHAR
        description: Name of sales representative
    
    time_dimensions:
      - name: order_date
        expr: ORDER_DATE
        data_type: DATE
    
    measures:
      - name: total_revenue
        expr: NET_AMOUNT
        data_type: NUMBER
        aggregation: sum
        description: Total net revenue after discounts
        
      - name: order_count
        expr: ORDER_ID
        data_type: NUMBER
        aggregation: count_distinct
        description: Number of unique orders
        
      - name: total_quantity
        expr: QUANTITY
        data_type: NUMBER
        aggregation: sum
        description: Total units sold
        
      - name: avg_order_value
        expr: NET_AMOUNT
        data_type: NUMBER
        aggregation: avg
        description: Average order value
        
      - name: customer_count
        expr: CUSTOMER_ID
        data_type: NUMBER
        aggregation: count_distinct
        description: Number of unique customers
```

### TR-6: Streamlit App Structure

```python
# app.py - Main entry point
# pages/
#   1_Overview.py      - Executive KPIs and summary
#   2_Trends.py        - Time series analysis
#   3_Regions.py       - Regional breakdown
#   4_Products.py      - Product performance
#   5_Team.py          - Sales rep leaderboard
# utils/
#   data.py            - Data fetching functions
#   charts.py          - Chart configurations
```

**Required Components**:
- Sidebar with global filters (date range, region, segment)
- KPI cards with delta indicators (vs prior period)
- Interactive charts (Plotly or Altair)
- Data tables with sorting/filtering
- Session state for filter persistence

---

## Feature Breakdown (Generate in Session 1)

Use these phases to organize the feature_list.json:

### Phase 1: Infrastructure (Features 1-10)
- Create database
- Create schemas (RAW, STAGING, MARTS, SEMANTIC)
- Create warehouse
- Set up file formats (if needed)
- Create roles (optional)

### Phase 2: Raw Data (Features 11-20)
- Create ORDERS table with sample data
- Create CUSTOMERS table with sample data
- Create PRODUCTS table with sample data
- Create SALES_REPS table with sample data
- Verify data quality in raw tables

### Phase 3: Staging (Features 21-30)
- Create STG_ORDERS view/table
- Create STG_CUSTOMERS view
- Create STG_PRODUCTS view
- Create STG_SALES_REPS view
- Add data validation logic

### Phase 4: Marts - Fact Table (Features 31-40)
- Create FCT_ORDERS Dynamic Table
- Join all dimensions
- Calculate NET_AMOUNT
- Add period columns (week, month, quarter, year)
- Verify joins and calculations

### Phase 5: Marts - Aggregations (Features 41-50)
- Create DAILY_SALES Dynamic Table
- Create SALES_BY_REGION Dynamic Table
- Create SALES_BY_PRODUCT Dynamic Table
- Create SALES_BY_CUSTOMER Dynamic Table
- Create SALES_BY_REP Dynamic Table

### Phase 6: Semantic Model (Features 51-60)
- Create sales_model.yaml
- Define all dimensions
- Define all measures
- Add time dimension configuration
- Test 5 required questions with Cortex Analyst

### Phase 7: Streamlit - Setup (Features 61-65)
- Create app.py scaffold
- Create sidebar with filters
- Create utils/data.py
- Create pages directory structure

### Phase 8: Streamlit - Pages (Features 66-75)
- Build Overview page with KPIs
- Build Trends page with time series
- Build Regions page with comparison
- Build Products page with breakdown
- Build Team page with leaderboard

### Phase 9: Polish (Features 76-80)
- Add error handling
- Add loading states
- Test all filters
- Verify data freshness
- Final validation

---

## Validation Checkpoints

### After Phase 2 (Raw Data):
```sql
SELECT 'ORDERS' as tbl, COUNT(*) as cnt FROM SALES_ANALYTICS_DB.RAW.ORDERS
UNION ALL SELECT 'CUSTOMERS', COUNT(*) FROM SALES_ANALYTICS_DB.RAW.CUSTOMERS
UNION ALL SELECT 'PRODUCTS', COUNT(*) FROM SALES_ANALYTICS_DB.RAW.PRODUCTS
UNION ALL SELECT 'SALES_REPS', COUNT(*) FROM SALES_ANALYTICS_DB.RAW.SALES_REPS;
-- Expected: ~100K, ~10K, ~500, ~50
```

### After Phase 5 (Marts):
```sql
SELECT COUNT(*) FROM SALES_ANALYTICS_DB.MARTS.FCT_ORDERS;
-- Expected: ~100K

SELECT REGION, SUM(NET_AMOUNT) as revenue 
FROM SALES_ANALYTICS_DB.MARTS.DAILY_SALES 
GROUP BY REGION;
-- Expected: 4 regions with reasonable revenue distribution
```

### After Phase 6 (Semantic Model):
Use Cortex Analyst to verify:
```
cortex analyst query "What was total revenue last month?" --model=semantic/sales_model.yaml
```

### After Phase 8 (Streamlit):
- Deploy app and verify URL is accessible
- Test all filters work
- Verify charts render with data

---

## Success Criteria

The project is **COMPLETE** when:

1. ✓ All 80 features in feature_list.json have `passes: true`
2. ✓ Dynamic Tables refresh within 5 minutes
3. ✓ All 5 Cortex Analyst test questions return correct answers
4. ✓ Streamlit app is deployed and all pages functional
5. ✓ cortex-progress.md shows 100% completion

---

## Notes for Agents

- **Be patient**: This project takes 10-20 sessions to complete
- **Be thorough**: Test everything before marking as passing
- **Be organized**: Follow the phase order, don't skip ahead
- **Be communicative**: Document everything in progress files
- **Be resilient**: If something breaks, fix it before continuing
