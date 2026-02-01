# Long-Running Agents with Cortex Code CLI

A comprehensive guide and reference implementation for building complex, multi-session projects using **Snowflake's Cortex Code CLI** with the **Long-Running Agent Pattern**.

This repository demonstrates the pattern through a complete Sales Analytics Platform built across 10 sessions with 80 tracked features.

---

## Table of Contents

1. [What is Cortex Code CLI?](#what-is-cortex-code-cli)
2. [Standard vs Long-Running Agent Approach](#standard-vs-long-running-agent-approach)
3. [The Long-Running Agent Pattern](#the-long-running-agent-pattern)
4. [Plan Mode vs Execution Mode](#plan-mode-vs-execution-mode)
5. [How to Use This Pattern](#how-to-use-this-pattern)
6. [Creating Your Own Specification File](#creating-your-own-specification-file)
7. [Progress Tracking Files](#progress-tracking-files)
8. [Session Workflow](#session-workflow)
9. [Reference Implementation](#reference-implementation)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## What is Cortex Code CLI?

**Cortex Code CLI** is Snowflake's AI-powered command-line interface for software development. It provides an interactive environment where developers collaborate with an AI agent to build applications, write SQL, and manage Snowflake resources.

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **SQL Execution** | Run queries directly against Snowflake |
| **File Operations** | Read, write, and edit code files |
| **Shell Commands** | Execute git, npm, and other CLI tools |
| **Web Search** | Research documentation and solutions |
| **Multi-tool Orchestration** | Combine tools for complex workflows |

### Basic Usage

```bash
# Start Cortex Code CLI
cortex

# Ask questions or give instructions
> "Create a Snowflake table for customer data"
> "Fix the error in my Python script"
> "Explain this SQL query"
```

---

## Standard vs Long-Running Agent Approach

### Standard Cortex Code CLI Approach

The standard approach works well for:
- Single-session tasks
- Small to medium projects (< 20 features)
- Quick fixes and queries
- Exploratory work

**Limitations:**
- Context window constraints (~100K tokens)
- No persistence between sessions
- Large projects exceed context capacity
- Previous decisions are forgotten

### Long-Running Agent Approach

The Long-Running Agent pattern solves these limitations for:
- Large projects (50-100+ features)
- Multi-day/multi-week efforts
- Complex systems with dependencies
- Projects requiring audit trails

**Key Differences:**

| Aspect | Standard Approach | Long-Running Agent |
|--------|------------------|-------------------|
| **Session Scope** | Complete in one session | Spans multiple sessions |
| **Context** | In-memory only | Persisted to files |
| **Progress** | Manual tracking | Structured JSON/Markdown |
| **Resumability** | Start over each time | Continue exactly where left off |
| **Audit Trail** | None | Complete session history |
| **Scale** | 10-20 features | 50-100+ features |
| **Consistency** | Varies by session | Enforced through validation |

---

## The Long-Running Agent Pattern

### Core Concept

The pattern breaks large projects into **incremental sessions**, each building on the previous through **structured progress files**.

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION 1 (Initialization)                                      │
│  ► Analyze specification document                                │
│  ► Generate feature_list.json (50-80 features)                   │
│  ► Create cortex-progress.md                                     │
│  ► Implement foundational features                               │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  SESSION 2+ (Incremental Progress)                               │
│  ► Read progress files to restore context                        │
│  ► Validate existing work still functions                        │
│  ► Implement next incomplete feature                             │
│  ► Test thoroughly                                               │
│  ► Update progress files                                         │
│  ► Leave clean state for next session                            │
└─────────────────────────────────────────────────────────────────┘
                              ▼
                    (Repeat until complete)
```

### Three Essential Components

| Component | Purpose | File |
|-----------|---------|------|
| **Specification** | Project requirements & agent instructions | `*_platform.md` |
| **Feature List** | Tracks all features with pass/fail status | `feature_list.json` |
| **Progress Log** | Session history and current state | `cortex-progress.md` |

---

## Plan Mode vs Execution Mode

Cortex Code CLI operates in two modes that work together for long-running projects:

### Plan Mode

**Purpose:** Design implementation strategy before writing code.

**When to Use:**
- Starting a new project or phase
- Complex features requiring architectural decisions
- When multiple approaches are possible

**How to Enter:**
```bash
# In Cortex Code CLI
> /plan
> Read @sales_analytics_platform.md and create an implementation plan
```

**What Happens:**
1. Agent explores codebase and requirements
2. Identifies existing patterns and constraints
3. Drafts step-by-step implementation plan
4. Presents plan for user approval
5. User can refine or approve

### Execution Mode

**Purpose:** Implement the approved plan by writing code.

**When to Use:**
- After plan is approved
- For well-defined tasks
- Continuing previous work

**How to Enter:**
```bash
# After plan approval, agent automatically exits to execution
# Or start directly for continuation:
> resume
```

**What Happens:**
1. Agent reads progress files
2. Identifies next incomplete feature
3. Implements feature completely
4. Tests and validates
5. Updates progress files

### Plan + Execution Workflow

```
┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│   PLAN MODE      │     │   USER REVIEW     │     │ EXECUTION MODE   │
│                  │     │                   │     │                  │
│ • Read specs     │────▶│ • Approve plan    │────▶│ • Write code     │
│ • Analyze reqs   │     │ • Request changes │     │ • Run tests      │
│ • Design approach│     │ • Ask questions   │     │ • Update progress│
│ • Create plan    │     │                   │     │ • Validate       │
└──────────────────┘     └───────────────────┘     └──────────────────┘
```

---

## How to Use This Pattern

### Step 1: Create Specification Document

Create a `<project_name>_platform.md` file following this structure:

```markdown
# Project Name - Long-Running Project Specification

## How to Execute This Project
[Instructions for the agent]

# PART 1: LONG-RUNNING AGENT PATTERN
[Pattern rules and workflow]

# PART 2: PROJECT REQUIREMENTS
[Business requirements, technical specs, feature breakdown]
```

See [sales_analytics_platform.md](sales_analytics_platform.md) for a complete example.

### Step 2: Start First Session (Plan Mode)

```bash
# Start Cortex Code CLI
cortex

# Enter plan mode with specification
> /plan
> Read @sales_analytics_platform.md and execute this long-running project 
> following the agent pattern defined in the document.
```

The agent will:
1. Analyze the specification
2. Generate `feature_list.json` with 50-80 features
3. Create `cortex-progress.md`
4. Implement initial features
5. Update progress files

### Step 3: Continue in Subsequent Sessions

```bash
# Option 1: Use continue flag
cortex --continue

# Option 2: Start fresh and reference progress
cortex
> resume

# Option 3: Explicit continuation
> /plan
> Continue the project. Read feature_list.json and cortex-progress.md 
> to understand current state, then implement the next incomplete feature.
```

### Step 4: Repeat Until Complete

Each session:
1. Reads progress files
2. Validates existing work
3. Implements 1-3 features
4. Updates progress
5. Ends cleanly

---

## Creating Your Own Specification File

### Template Structure

```markdown
# [Project Name] - Long-Running Project Specification

## How to Execute This Project

This project uses the **Long-Running Agents Pattern** for complex, 
multi-session work.

### Starting the Project (First Session)
\`\`\`
/plan
Read @[filename].md and execute this long-running project following 
the agent pattern defined in the document.
\`\`\`

### Continuing the Project (Subsequent Sessions)
\`\`\`
resume
\`\`\`

---

# PART 1: LONG-RUNNING AGENT PATTERN

## Overview
[Explain the incremental approach]

## Critical Rules
1. **ONE FEATURE AT A TIME** - Never implement multiple features at once
2. **TEST EVERYTHING** - Features must be verified before marking complete
3. **DOCUMENT THOROUGHLY** - Next session has no memory of current work
4. **NEVER BREAK EXISTING** - Validate before adding new features
5. **LEAVE CLEAN STATE** - No half-implemented code

## Required Artifacts

### 1. feature_list.json
[JSON structure with id, phase, priority, title, passes, tested_at, notes]

### 2. cortex-progress.md
[Markdown structure with status, session history, objects created]

## Session Workflow
[Step-by-step workflow for each session]

---

# PART 2: PROJECT REQUIREMENTS

## Business Context
[Goals, users, key questions to answer]

## Functional Requirements
[FR-1, FR-2, etc. with checkboxes]

## Technical Requirements
[Architecture, schemas, configurations]

## Feature Breakdown
[Phase 1: Features 1-10, Phase 2: Features 11-20, etc.]

## Validation Checkpoints
[SQL queries and tests for each phase]

## Success Criteria
[Definition of done]
```

### Key Sections Explained

#### Critical Rules Section
```markdown
## Critical Rules

1. **ONE FEATURE AT A TIME** - Focus prevents errors and ensures quality
2. **TEST EVERYTHING** - A feature is not done until verified
3. **DOCUMENT THOROUGHLY** - The next session has NO memory
4. **NEVER BREAK EXISTING** - Always validate before adding
5. **LEAVE CLEAN STATE** - No half-implemented code
```

#### Feature Breakdown Section
```markdown
## Feature Breakdown

### Phase 1: Infrastructure (Features 1-10)
- Create database
- Create schemas
- Create warehouse
- Verify connectivity

### Phase 2: Data Layer (Features 11-20)
- Create source tables
- Load sample data
- Create staging views
- Add data quality checks

### Phase 3: Business Logic (Features 21-30)
[Continue pattern...]
```

#### Validation Checkpoints Section
```markdown
## Validation Checkpoints

### After Phase 2:
\`\`\`sql
SELECT COUNT(*) FROM schema.table;
-- Expected: ~10,000 rows
\`\`\`

### After Phase 3:
\`\`\`sql
SELECT SUM(amount) FROM schema.aggregated_table;
-- Expected: Matches source total
\`\`\`
```

---

## Progress Tracking Files

### feature_list.json

Tracks every feature with status:

```json
{
  "project": "Your Project Name",
  "created": "2024-01-15T10:00:00Z",
  "total_features": 80,
  "features": [
    {
      "id": 1,
      "phase": "infrastructure",
      "priority": 1,
      "title": "Create database",
      "description": "Create main database for the platform",
      "acceptance_criteria": [
        "Database exists",
        "Current role has access"
      ],
      "passes": true,
      "tested_at": "2024-01-15T10:30:00Z",
      "notes": "Created successfully"
    },
    {
      "id": 2,
      "phase": "infrastructure", 
      "priority": 1,
      "title": "Create schemas",
      "passes": false,
      "tested_at": null,
      "notes": ""
    }
  ]
}
```

**Field Definitions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Unique feature identifier |
| `phase` | string | Project phase (infrastructure, data, etc.) |
| `priority` | number | 1 = must have, 2 = nice to have |
| `title` | string | Short feature name |
| `description` | string | Detailed description |
| `acceptance_criteria` | array | Conditions for completion |
| `passes` | boolean | Whether feature is complete |
| `tested_at` | string | ISO timestamp of last test |
| `notes` | string | Implementation notes |

### cortex-progress.md

Session history and current state:

```markdown
# Project Name - Progress Log

## Quick Status
- **Total Features**: 80
- **Completed**: 45
- **Remaining**: 35
- **Last Updated**: 2024-01-20T15:30:00Z

## Session History

### Session 5 - 2024-01-20
- **Type**: Data Layer Implementation
- **Features Completed**: #21, #22, #23
- **Objects Created**: 
  - VIEW: STAGING.STG_ORDERS
  - VIEW: STAGING.STG_CUSTOMERS
- **Issues**: None
- **Next**: Implement feature #24 (Create fact table)

### Session 4 - 2024-01-19
[Previous session details...]

---

## Current Objects

| Type | Name | Schema | Status |
|------|------|--------|--------|
| DATABASE | MY_DB | - | ✓ |
| SCHEMA | RAW | MY_DB | ✓ |
| TABLE | ORDERS | RAW | ✓ (100K rows) |

## Known Issues / Blockers
- Issue #1: [Description and workaround]

## Validation Queries
\`\`\`sql
-- Verify row counts
SELECT COUNT(*) FROM MY_DB.RAW.ORDERS;
\`\`\`
```

---

## Session Workflow

### Starting a Session

```
┌─────────────────────────────────────────────────────────────┐
│ 1. READ PROGRESS FILES                                       │
│    • cortex-progress.md - What was done, what's next        │
│    • feature_list.json - Find next incomplete feature       │
├─────────────────────────────────────────────────────────────┤
│ 2. VALIDATE EXISTING WORK                                    │
│    • Run validation queries                                  │
│    • Verify objects exist                                    │
│    • Check for any regressions                              │
├─────────────────────────────────────────────────────────────┤
│ 3. SELECT NEXT FEATURE                                       │
│    • Lowest ID where passes: false                          │
│    • Respect phase dependencies                              │
├─────────────────────────────────────────────────────────────┤
│ 4. IMPLEMENT FEATURE                                         │
│    • Write code/SQL                                          │
│    • Follow existing patterns                                │
│    • Handle edge cases                                       │
├─────────────────────────────────────────────────────────────┤
│ 5. TEST FEATURE                                              │
│    • Run acceptance criteria                                 │
│    • Verify with queries                                     │
│    • Check for side effects                                  │
├─────────────────────────────────────────────────────────────┤
│ 6. UPDATE PROGRESS                                           │
│    • Mark feature passes: true                              │
│    • Update cortex-progress.md                              │
│    • Document any issues                                     │
├─────────────────────────────────────────────────────────────┤
│ 7. END CLEANLY                                               │
│    • Note next steps                                         │
│    • Ensure no broken state                                  │
│    • Commit if using git                                     │
└─────────────────────────────────────────────────────────────┘
```

### Handling Context Exhaustion

If you run out of context mid-session:

1. **Immediately update progress files** with current state
2. **Document exactly where you stopped**
3. **Note any partial work** that needs completion
4. **Start new session** with `resume`

```markdown
### Session 7 - 2024-01-22 (PARTIAL)
- **Type**: Feature Implementation
- **Features Attempted**: #35
- **Status**: INCOMPLETE - Context exhausted
- **Partial Work**: 
  - Created table structure
  - Did NOT populate data
- **Resume Point**: Continue #35 - add INSERT statement
```

---

## Reference Implementation

This repository contains a complete Sales Analytics Platform demonstrating the pattern:

### Project Statistics

| Metric | Value |
|--------|-------|
| Total Features | 80 |
| Sessions | 10 |
| Completion | 90% (72/80) |
| P1 Features | 100% complete |
| Snowflake Objects | 16 |
| Streamlit Pages | 6 |

### File Structure

```
├── README.md                      # This guide
├── sales_analytics_platform.md   # Specification document (template)
├── feature_list.json             # Feature tracking
├── cortex-progress.md            # Session history
├── snowflake_setup.sql           # All Snowflake DDL/DML
├── sales_model.yaml              # Cortex Analyst semantic model
│
└── streamlit_app/                # Streamlit application
    ├── streamlit_app.py
    └── app_pages/
        ├── executive_dashboard.py
        ├── regional_analysis.py
        ├── product_analysis.py
        ├── sales_rep_leaderboard.py
        ├── customer_insights.py
        └── cortex_analyst.py
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/curious-bigcat/snowflake-cortex-code-long-running-agents.git
cd snowflake-cortex-code-long-running-agents

# Review the specification
cat sales_analytics_platform.md

# Start your own project using this as a template
cp sales_analytics_platform.md my_project_platform.md
# Edit my_project_platform.md with your requirements

# Start Cortex Code CLI
cortex

# Begin with plan mode
> /plan
> Read @my_project_platform.md and execute this long-running project
```

---

## Best Practices

### Do's

| Practice | Why |
|----------|-----|
| ✅ One feature per session | Reduces errors, ensures quality |
| ✅ Test before marking complete | Prevents false progress |
| ✅ Update progress immediately | Maintains accurate state |
| ✅ Document blockers | Helps future sessions |
| ✅ Use validation checkpoints | Catches regressions early |
| ✅ Follow phase order | Respects dependencies |

### Don'ts

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| ❌ Skip testing | Creates technical debt |
| ❌ Implement multiple features | Increases error risk |
| ❌ Forget to update progress | Loses work tracking |
| ❌ Leave broken state | Blocks next session |
| ❌ Skip ahead in phases | Breaks dependencies |
| ❌ Delete features from list | Loses audit trail |

### Priority System

Use P1/P2 to manage scope:

- **P1 (Priority 1)**: Core functionality - must complete for MVP
- **P2 (Priority 2)**: Enhancements - implement after P1 complete

This allows shipping a working product while tracking desired improvements.

---

## Troubleshooting

### Common Issues

#### "Context exhausted mid-feature"

**Solution:**
1. Update progress files immediately
2. Document partial work in notes
3. Start new session with `resume`
4. Agent will read state and continue

#### "Feature marked complete but doesn't work"

**Solution:**
1. Set `passes: false` in feature_list.json
2. Add notes explaining the issue
3. Re-implement in next session
4. Run validation queries before marking complete

#### "Lost track of what's done"

**Solution:**
1. Run validation queries from specification
2. Check cortex-progress.md for object list
3. Query Snowflake: `SHOW TABLES IN DATABASE`
4. Reconcile with feature_list.json

#### "Snowflake connection issues"

**Solution:**
1. Document in cortex-progress.md under "Known Issues"
2. Focus on code-only work (no SQL execution)
3. Queue SQL work for when connection restored
4. Note specific features blocked

### Recovery Commands

```sql
-- Check what exists in Snowflake
SHOW DATABASES LIKE 'MY_PROJECT%';
SHOW SCHEMAS IN DATABASE MY_PROJECT_DB;
SHOW TABLES IN SCHEMA MY_PROJECT_DB.MARTS;
SHOW DYNAMIC TABLES IN SCHEMA MY_PROJECT_DB.MARTS;

-- Verify row counts
SELECT 'TABLE1' as name, COUNT(*) as rows FROM MY_PROJECT_DB.RAW.TABLE1
UNION ALL SELECT 'TABLE2', COUNT(*) FROM MY_PROJECT_DB.RAW.TABLE2;
```

---

## Adapting for Your Project

### Step-by-Step

1. **Copy the specification template**
   ```bash
   cp sales_analytics_platform.md my_project_platform.md
   ```

2. **Update Part 1** - Keep the pattern, update project name

3. **Rewrite Part 2** - Your requirements:
   - Business context
   - Functional requirements
   - Technical requirements
   - Feature breakdown (aim for 50-80 features)
   - Validation checkpoints

4. **Start with Cortex Code CLI**
   ```bash
   cortex
   > /plan
   > Read @my_project_platform.md and execute this long-running project
   ```

5. **Continue sessions** with `resume`

### Example Project Types

This pattern works for:

- **Data Warehouses**: ETL pipelines, dimensional models
- **Analytics Platforms**: Dashboards, reports, semantic models
- **Data Applications**: Streamlit/Gradio apps with Snowflake backend
- **ML Pipelines**: Feature engineering, model training workflows
- **Migration Projects**: Legacy system to Snowflake migrations

---

## License

MIT License - Feel free to use this pattern for your projects.

---

## Resources

- [Cortex Code CLI Documentation](https://docs.snowflake.com/user-guide/snowflake-cortex/cortex-agents)
- [Snowflake Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-intro)
- [Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)

---

*Built with Cortex Code CLI - Snowflake's AI-powered development assistant*
