# Sales Analytics Platform

A comprehensive sales analytics solution built on Snowflake using the **Long-Running Agent Pattern** with **Cortex Code CLI**. This project demonstrates how to build production-grade data platforms iteratively across multiple sessions while maintaining context, progress, and quality.

---

## Table of Contents

1. [Overview](#overview)
2. [What is Cortex Code CLI?](#what-is-cortex-code-cli)
3. [What are Long-Running Agents?](#what-are-long-running-agents)
4. [Why Use Long-Running Agents?](#why-use-long-running-agents)
5. [Project Architecture](#project-architecture)
6. [Implementation Approach](#implementation-approach)
7. [Project Structure](#project-structure)
8. [Phase-by-Phase Implementation](#phase-by-phase-implementation)
9. [Progress Tracking System](#progress-tracking-system)
10. [How to Resume Work](#how-to-resume-work)
11. [Validation & Testing](#validation--testing)
12. [Lessons Learned](#lessons-learned)
13. [Quick Start](#quick-start)

---

## Overview

The Sales Analytics Platform is a full-stack analytics solution that includes:

- **Snowflake Data Warehouse**: Multi-layer architecture (RAW → STAGING → MARTS)
- **Dynamic Tables**: Real-time data transformation with 5-minute refresh
- **Semantic Model**: Natural language queries via Cortex Analyst
- **Streamlit Dashboard**: Interactive 6-page analytics application

**Key Metrics:**
- 80 features across 9 phases
- 100,000 orders, 10,000 customers, 500 products, 50 sales reps
- ~$394M total revenue over 2 years of data
- Built across 10 sessions using the Long-Running Agent Pattern

---

## What is Cortex Code CLI?

**Cortex Code CLI** is Snowflake's official command-line interface for AI-assisted software development. It provides an interactive environment where developers can collaborate with an AI agent to:

- Write, debug, and refactor code
- Execute SQL queries against Snowflake
- Create and modify files
- Run shell commands
- Build complete applications iteratively

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-tool Access** | File operations, SQL execution, web search, shell commands |
| **Context Awareness** | Understands your codebase, project structure, and history |
| **Snowflake Integration** | Direct connection to Snowflake for SQL execution |
| **Session Continuity** | Can resume work across multiple sessions |
| **Progress Tracking** | Built-in todo list and task management |

### Basic Usage

```bash
# Start Cortex Code CLI
cortex-code

# Common interactions
> "Create a new Streamlit app for sales analytics"
> "Fix the SQL error in my dashboard"
> "Resume"  # Continue from previous session
```

---

## What are Long-Running Agents?

**Long-Running Agents** represent a pattern for executing complex, multi-session projects with AI assistance. Unlike simple one-off queries, long-running agents:

1. **Persist context** across multiple sessions
2. **Track progress** through structured files
3. **Resume work** exactly where left off
4. **Maintain quality** through validation checkpoints

### The Pattern

```
Session 1 → Progress File → Session 2 → Progress File → Session 3 → ...
    ↓                           ↓                           ↓
 Features                   Features                    Features
  1-10                       11-30                       31-50
```

### Key Components

| Component | Purpose | File |
|-----------|---------|------|
| **Feature List** | Tracks all features with pass/fail status | `feature_list.json` |
| **Progress Log** | Session history and changes made | `cortex-progress.md` |
| **Specification** | Project requirements and architecture | `sales_analytics_platform.md` |

---

## Why Use Long-Running Agents?

### Problem: Context Window Limitations

AI assistants have context window limits. For large projects:
- Code exceeds context capacity
- Previous decisions are forgotten
- Work must be repeated
- Consistency is lost

### Solution: Structured Progress Tracking

Long-running agents solve this by:

| Challenge | Solution |
|-----------|----------|
| Context limits | Progress files summarize state |
| Lost decisions | Feature list captures outcomes |
| Repeated work | Session logs track what's done |
| Inconsistency | Validation checkpoints ensure quality |

### Benefits

1. **Scalability**: Build projects of any size
2. **Reliability**: Never lose progress
3. **Quality**: Systematic validation at each phase
4. **Flexibility**: Pause and resume anytime
5. **Transparency**: Full audit trail of changes

### When to Use

- Projects requiring 50+ features
- Multi-day implementation efforts
- Complex systems with dependencies
- Projects needing validation checkpoints
- Team handoffs or documentation requirements

---

## Project Architecture

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        SNOWFLAKE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐   │
│  │   RAW   │ → │ STAGING  │ → │  MARTS  │ → │ SEMANTIC │   │
│  │ Tables  │    │  Views   │    │ Dynamic │    │  Model   │   │
│  └─────────┘    └──────────┘    │ Tables  │    └──────────┘   │
│       ↑                         └─────────┘          ↓         │
│   Source                             ↓          Cortex        │
│    Data                         ┌─────────┐    Analyst        │
│                                 │   Agg   │                   │
│                                 │ Tables  │                   │
│                                 └─────────┘                   │
│                                      ↓                         │
└──────────────────────────────────────┼─────────────────────────┘
                                       ↓
                            ┌─────────────────────┐
                            │   STREAMLIT APP     │
                            ├─────────────────────┤
                            │ • Executive Dashboard│
                            │ • Regional Analysis  │
                            │ • Product Analysis   │
                            │ • Sales Leaderboard  │
                            │ • Customer Insights  │
                            │ • Cortex Analyst     │
                            └─────────────────────┘
```

### Schema Design

| Schema | Purpose | Objects |
|--------|---------|---------|
| **RAW** | Source data ingestion | CUSTOMERS, PRODUCTS, SALES_REPS, ORDERS |
| **STAGING** | Data cleansing & validation | STG_* views with IS_VALID flags |
| **MARTS** | Business-ready aggregations | FCT_ORDERS + 5 aggregation tables |
| **SEMANTIC** | AI query interface | sales_model.yaml |

### Dynamic Tables

All mart tables use Snowflake Dynamic Tables with:
- **Target Lag**: 5 minutes
- **Refresh Mode**: Auto
- **Warehouse**: SALES_ANALYTICS_WH (SMALL)

---

## Implementation Approach

### Phase-Based Development

The project was implemented in 9 phases, each with specific deliverables:

```
Phase 1: Infrastructure     → Database, Schemas, Warehouse
Phase 2: Raw Data          → Tables + Sample Data (100K orders)
Phase 3: Staging           → Cleansing Views + Quality Flags
Phase 4: Marts Fact        → FCT_ORDERS Dynamic Table
Phase 5: Marts Aggregation → 5 Aggregation Dynamic Tables
Phase 6: Semantic Model    → Cortex Analyst YAML
Phase 7: Streamlit Setup   → App Structure + Navigation
Phase 8: Streamlit Pages   → 6 Interactive Dashboards
Phase 9: Polish            → Error Handling + UX
```

### Priority System

Features were tagged with priorities:
- **P1 (Priority 1)**: Core functionality - must complete
- **P2 (Priority 2)**: Enhancements - nice to have

This allowed the project to reach "usable" state quickly while deferring optimizations.

### Validation Checkpoints

Each phase ended with validation:

```sql
-- Example: Phase 5 Validation
SELECT 
    'FCT_ORDERS' as table_name, 
    SUM(NET_AMOUNT) as revenue 
FROM MARTS.FCT_ORDERS
UNION ALL
SELECT 'DAILY_SALES', SUM(REVENUE) FROM MARTS.DAILY_SALES;
-- Both should equal ~$394M
```

---

## Project Structure

```
longrunning_agents/
├── README.md                      # This file
├── sales_analytics_platform.md   # Project specification
├── feature_list.json             # Feature tracking (80 features)
├── cortex-progress.md            # Session history log
├── snowflake_setup.sql           # All Snowflake DDL/DML
├── sales_model.yaml              # Cortex Analyst semantic model
│
└── streamlit_app/                # Streamlit application
    ├── streamlit_app.py          # Main app with navigation
    ├── .streamlit/
    │   └── secrets.toml          # Snowflake connection config
    └── app_pages/
        ├── executive_dashboard.py # KPIs and trends
        ├── regional_analysis.py   # Regional breakdown
        ├── product_analysis.py    # Category/product metrics
        ├── sales_rep_leaderboard.py # Rep rankings
        ├── customer_insights.py   # Customer segments
        └── cortex_analyst.py      # Natural language queries
```

### Key Files Explained

| File | Purpose |
|------|---------|
| `feature_list.json` | JSON array of 80 features with id, title, priority, passes, tested_at, notes |
| `cortex-progress.md` | Markdown log of each session: what was done, files changed, issues encountered |
| `snowflake_setup.sql` | Complete SQL to recreate all Snowflake objects from scratch |
| `sales_model.yaml` | Semantic model defining dimensions, measures, and time dimensions for Cortex Analyst |

---

## Phase-by-Phase Implementation

### Phase 1: Infrastructure (Session 1)

**Features**: #1-#10 (7 P1, 3 P2)

```sql
-- Created database and schemas
CREATE DATABASE SALES_ANALYTICS_DB;
CREATE SCHEMA RAW;
CREATE SCHEMA STAGING;
CREATE SCHEMA MARTS;
CREATE SCHEMA SEMANTIC;

-- Created warehouse
CREATE WAREHOUSE SALES_ANALYTICS_WH
    WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 120;
```

**Outcome**: Foundation ready for data loading

---

### Phase 2: Raw Data (Session 2)

**Features**: #11-#20 (10 P1)

Created and populated 4 tables:

| Table | Rows | Key Attributes |
|-------|------|----------------|
| CUSTOMERS | 10,000 | Segment distribution: Enterprise 10%, SMB 30%, Consumer 60% |
| PRODUCTS | 500 | 10 categories, prices $10-$5,000 |
| SALES_REPS | 50 | 4 regions: North, South, East, West |
| ORDERS | 100,000 | 2 years of data, 10% with discounts |

**Outcome**: Raw data layer complete with realistic sample data

---

### Phase 3: Staging (Session 3)

**Features**: #21-#30 (8 P1, 2 P2)

Created staging views with:
- Data type standardization
- Calculated fields (NET_AMOUNT, GROSS_AMOUNT)
- Date part extraction (ORDER_WEEK, ORDER_MONTH, etc.)
- Data quality flags (IS_VALID)

```sql
CREATE VIEW STAGING.STG_ORDERS AS
SELECT 
    *,
    QUANTITY * UNIT_PRICE * (1 - DISCOUNT_PCT) AS NET_AMOUNT,
    DATE_TRUNC('month', ORDER_DATE) AS ORDER_MONTH,
    CASE WHEN ... THEN TRUE ELSE FALSE END AS IS_VALID
FROM RAW.ORDERS;
```

**Outcome**: Clean, validated data ready for mart layer

---

### Phase 4: Marts Fact Table (Session 4)

**Features**: #31-#40 (10 P1)

Created FCT_ORDERS Dynamic Table joining all dimensions:

```sql
CREATE DYNAMIC TABLE MARTS.FCT_ORDERS
    TARGET_LAG = '5 minutes'
    WAREHOUSE = SALES_ANALYTICS_WH
AS
SELECT 
    o.*, c.CUSTOMER_NAME, c.SEGMENT,
    p.PRODUCT_NAME, p.CATEGORY,
    r.REP_NAME, r.REGION
FROM STAGING.STG_ORDERS o
LEFT JOIN STAGING.STG_CUSTOMERS c ON ...
LEFT JOIN STAGING.STG_PRODUCTS p ON ...
LEFT JOIN STAGING.STG_SALES_REPS r ON ...;
```

**Validation**: 0 NULL values in dimension joins, total revenue = $393.96M

**Outcome**: Central fact table with all dimensions denormalized

---

### Phase 5: Aggregation Tables (Session 5)

**Features**: #41-#50 (8 P1, 2 P2)

Created 5 aggregation Dynamic Tables:

| Table | Grain | Rows | Purpose |
|-------|-------|------|---------|
| DAILY_SALES | Day | 2,920 | Time series trends |
| SALES_BY_REGION | Region + Month | 96 | Geographic analysis |
| SALES_BY_PRODUCT | Product + Month | 1,500 | Product performance |
| SALES_BY_CUSTOMER | Customer | 9,999 | Customer value |
| SALES_BY_REP | Rep + Month | 150 | Sales performance |

**Validation**: All tables sum to $393.96M baseline

**Outcome**: Pre-aggregated tables for fast dashboard queries

---

### Phase 6: Semantic Model (Session 6)

**Features**: #51-#60 (9 P1, 1 P2)

Created sales_model.yaml with:
- **15 Dimensions**: customer, product, rep, region, segment, industry, etc.
- **12 Measures**: revenue, gross_revenue, order_count, units_sold, AOV, etc.
- **5 Time Dimensions**: date, week, month, quarter, year

Tested with Cortex Analyst:
```
Q: "What was total revenue last month?"
A: December 2025: $16.3M from 4,045 orders

Q: "Top 10 products by revenue"
A: Product_0004 (SPORTS) leads at $6.08M

Q: "Sales by region"
A: North $102.3M, South $101.6M, West $96M, East $94.1M
```

**Outcome**: Natural language query interface ready

---

### Phase 7 & 8: Streamlit Application (Session 7)

**Features**: #61-#75 (14 P1, 1 P2)

Built 6-page Streamlit application:

1. **Executive Dashboard**: KPIs, revenue trends, regional breakdown
2. **Regional Analysis**: Region comparison, monthly trends
3. **Product Analysis**: Category performance, top products
4. **Sales Rep Leaderboard**: Rankings, individual performance
5. **Customer Insights**: Segment analysis, top customers
6. **Cortex Analyst**: Natural language query interface

Key patterns:
```python
# Connection handling
conn = st.connection("snowflake")

# Caching with TTL
@st.cache_data(ttl=timedelta(minutes=5))
def get_data(_conn, start, end):
    return _conn.query(sql)

# Session state for filters
st.session_state.date_start = start_date
st.session_state.date_end = end_date
```

**Outcome**: Fully functional interactive dashboard

---

### Phase 9: Polish (Sessions 8-10)

**Features**: #76-#80 (3 P1, 2 P2)

Added production-ready features:
- **Error handling**: try/except with st.error() on all pages
- **Loading states**: st.spinner() for user feedback
- **Drill-down**: st.expander() for detailed data
- **Documentation**: About section in sidebar
- **Data validation**: Date range checks, empty state handling

**Bug Fixes** (Session 10):
- Fixed column name mismatches (MONTH → ORDER_MONTH)
- Updated queries to use FCT_ORDERS directly
- Added type conversion for Decimal columns

**Outcome**: Production-ready application

---

## Progress Tracking System

### feature_list.json Structure

```json
{
  "project": "Sales Analytics Platform",
  "total_features": 80,
  "features": [
    {
      "id": 1,
      "phase": "infrastructure",
      "priority": 1,
      "title": "Create database SALES_ANALYTICS_DB",
      "description": "Create the main database...",
      "acceptance_criteria": ["Database exists", "Role has privileges"],
      "passes": true,
      "tested_at": "2026-01-31T06:26:22Z",
      "notes": "Database created successfully"
    }
  ]
}
```

### cortex-progress.md Structure

```markdown
## Quick Status
- **Total Features**: 80
- **Completed**: 72
- **Remaining**: 8 (all Priority 2)

## Session History

### Session 10 - 2026-02-01
- **Type**: Bug Fix
- **Issue**: SQL compilation error - invalid identifier 'MONTH'
- **Files Fixed**: executive_dashboard.py, regional_analysis.py
- **Status**: Bug fixed

### Session 9 - 2026-02-01
- **Type**: Priority 2 Enhancements
- **Features Completed**: #74, #78, #79
...
```

---

## How to Resume Work

### Starting a New Session

When returning to the project:

1. **Say "resume"** to Cortex Code CLI
2. The agent reads `cortex-progress.md` and `feature_list.json`
3. Context is reconstructed from progress files
4. Work continues from the last checkpoint

### What Gets Preserved

| Information | Storage Location |
|-------------|------------------|
| Completed features | feature_list.json (passes: true) |
| Session history | cortex-progress.md |
| Snowflake objects | Database (persistent) |
| Code files | Local filesystem |
| Configuration | secrets.toml, SQL files |

### Best Practices

1. **Update progress files** after each significant change
2. **Run validation queries** at phase boundaries
3. **Document blockers** in notes field
4. **Mark features complete** immediately when done

---

## Validation & Testing

### Row Count Validation

```sql
SELECT 'RAW.ORDERS' as tbl, COUNT(*) FROM RAW.ORDERS
UNION ALL SELECT 'MARTS.FCT_ORDERS', COUNT(*) FROM MARTS.FCT_ORDERS;
-- Both should be 100,000
```

### Revenue Baseline Validation

```sql
SELECT SUM(NET_AMOUNT) as total_revenue FROM MARTS.FCT_ORDERS;
-- Should be ~$393,961,464.45
```

### Dynamic Table Status

```sql
SHOW DYNAMIC TABLES IN SCHEMA MARTS;
-- All should show SCHEDULING_STATE = 'ACTIVE'
```

### Streamlit Testing

```bash
cd streamlit_app
streamlit run streamlit_app.py
# Verify all 6 pages load without errors
```

---

## Lessons Learned

### What Worked Well

1. **Phase-based approach**: Clear milestones and validation points
2. **Priority system**: P1/P2 allowed shipping core functionality first
3. **Progress files**: Essential for multi-session continuity
4. **Dynamic Tables**: Simplified ETL with auto-refresh
5. **FCT_ORDERS as single source**: Consistent data across all pages

### Challenges Encountered

| Challenge | Solution |
|-----------|----------|
| Connection timeouts | Focus on code-only changes when Snowflake unavailable |
| Column name mismatches | Query FCT_ORDERS directly with known schema |
| Decimal type handling | Explicit .astype(float) conversion |
| File edit conflicts | Sequential edits instead of parallel |

### Recommendations

1. **Document schema early**: Create DDL file before building queries
2. **Test queries independently**: Validate SQL before embedding in app
3. **Use explicit type casts**: Snowflake Decimals need conversion in Python
4. **Keep progress updated**: Update files immediately, not in batches

---

## Quick Start

### Prerequisites

- Snowflake account with ACCOUNTADMIN or equivalent
- Python 3.8+ with streamlit, snowflake-connector-python
- Cortex Code CLI installed

### Setup Steps

1. **Create Snowflake Objects**
   ```bash
   # In Snowflake worksheet or SnowSQL
   !source snowflake_setup.sql
   ```

2. **Upload Semantic Model**
   ```sql
   PUT file://./sales_model.yaml @SEMANTIC.SEMANTIC_MODELS AUTO_COMPRESS=FALSE;
   ```

3. **Configure Streamlit**
   ```bash
   # Edit streamlit_app/.streamlit/secrets.toml
   [connections.snowflake]
   account = "your-account"
   user = "your-user"
   password = "your-password"
   warehouse = "SALES_ANALYTICS_WH"
   database = "SALES_ANALYTICS_DB"
   schema = "MARTS"
   ```

4. **Run Application**
   ```bash
   cd streamlit_app
   streamlit run streamlit_app.py
   ```

### Resuming Development

```bash
# Start Cortex Code CLI
cortex-code

# In the CLI, say:
> resume

# The agent will read progress files and continue where you left off
```

---

## Project Status

| Metric | Value |
|--------|-------|
| Total Features | 80 |
| Completed | 72 (90%) |
| Priority 1 Complete | 100% |
| Priority 2 Complete | 37.5% |
| Sessions | 10 |
| Snowflake Objects | 16 |
| Streamlit Pages | 6 |

### Remaining P2 Features

- #8: Create stage for semantic model
- #9: Set default warehouse context
- #10: Infrastructure validation checkpoint
- #27: Add data quality flags to staging views
- #28: Create data quality summary view
- #47: Add running totals
- #48: Add moving averages
- #59: Add verified queries to semantic model

---

## License

This project was created as a demonstration of the Long-Running Agent Pattern with Cortex Code CLI.

---

*Built with Cortex Code CLI - Snowflake's AI-powered development assistant*
