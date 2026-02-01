# Building Complex Data Platforms with AI: The Long-Running Agent Pattern for Snowflake

## How I Built an 80-Feature Sales Analytics Platform Across 10 Sessions Using Cortex Code CLI

*A practical guide to breaking through AI context limitations and delivering production-grade data solutions*

---

![Header Image Placeholder](https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200)

---

Have you ever started an ambitious project with an AI coding assistant, only to hit a wall when the conversation got too long? You're deep into building something complex, the AI forgets what you discussed earlier, and suddenly you're explaining the same context over and over again.

I recently faced this exact challenge while building a comprehensive Sales Analytics Platform on Snowflake. The project required 80 distinct features across 9 phases—far too large for any single AI session. Instead of fighting the limitations, I developed a pattern that turned them into a strength.

**The result?** A complete, production-ready analytics platform built across 10 sessions with full context preservation, zero lost work, and a reusable pattern for any complex project.

In this article, I'll share exactly how I did it using **Snowflake's Cortex Code CLI** and what I call the **Long-Running Agent Pattern**.

---

## The Problem: AI Context Windows Have Limits

Modern AI coding assistants are incredibly powerful. They can write code, debug issues, explain complex systems, and even architect solutions. But they all share one fundamental limitation: **context windows**.

Every AI model has a maximum amount of information it can "remember" in a single conversation—typically measured in tokens (roughly 4 characters per token). Once you exceed this limit, older context gets pushed out, and the AI loses track of:

- Previous decisions you made together
- Code it wrote earlier in the session
- The overall architecture and patterns
- Why certain choices were made

For small projects, this isn't a problem. But for anything substantial—a data warehouse, a full-stack application, a complex ETL pipeline—you'll hit this wall fast.

### What Happens Without a Solution

Here's what typically happens when developers try to build large projects with AI assistants:

1. **Session 1**: Great progress! Built the foundation, feeling optimistic.
2. **Session 2**: Wait, why doesn't the AI remember our architecture decisions?
3. **Session 3**: Spent 30 minutes re-explaining context before any real work.
4. **Session 4**: The AI suggested something that contradicts our earlier approach.
5. **Session 5**: Gave up and did it manually.

Sound familiar?

---

## The Solution: Long-Running Agent Pattern

The Long-Running Agent Pattern solves this by **externalizing context to files** that persist between sessions. Instead of relying on the AI's memory, you create structured documents that capture:

- Every feature to be built (with pass/fail status)
- Session history (what was done, what's next)
- Current system state (objects created, validations passed)
- Known issues and blockers

Each session, the AI reads these files to restore full context, then updates them before ending. The result is **seamless continuity across unlimited sessions**.

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION 1                                                       │
│  • Read specification                                            │
│  • Generate feature list (80 features)                           │
│  • Create progress tracking                                      │
│  • Build foundation                                              │
│  • Update progress files ─────────────────┐                      │
└─────────────────────────────────────────────┼─────────────────────┘
                                              │
                    ┌─────────────────────────▼─────────────────────┐
                    │  feature_list.json    cortex-progress.md     │
                    │  (Persistent State)                          │
                    └─────────────────────────┬─────────────────────┘
                                              │
┌─────────────────────────────────────────────┼─────────────────────┐
│  SESSION 2                                  │                     │
│  • Read progress files ◄────────────────────┘                     │
│  • Validate existing work                                         │
│  • Implement next feature                                         │
│  • Test thoroughly                                                │
│  • Update progress files ─────────────────┐                       │
└─────────────────────────────────────────────┼─────────────────────┘
                                              │
                                              ▼
                                    (Repeat until done)
```

---

## Enter Cortex Code CLI

Before diving deeper into the pattern, let me introduce the tool that makes this possible: **Cortex Code CLI**.

Cortex Code CLI is Snowflake's AI-powered command-line interface for software development. Think of it as having a senior developer pair-programming with you who can:

- **Execute SQL** directly against Snowflake
- **Read and write files** in your project
- **Run shell commands** (git, npm, python, etc.)
- **Search the web** for documentation
- **Orchestrate complex workflows** combining all of the above

### Basic Usage

```bash
# Start Cortex Code CLI
cortex

# Now you're in an interactive session
> Create a Snowflake table for storing customer orders
> Fix the bug in my Python script at line 45
> Explain what this SQL query does
```

What makes Cortex Code CLI particularly powerful for long-running projects is its **Plan Mode** and **Execution Mode**—two complementary ways of working that map perfectly to the Long-Running Agent Pattern.

---

## Plan Mode vs Execution Mode

### Plan Mode: Think Before You Build

Plan Mode is for **designing before implementing**. When you enter Plan Mode, Cortex Code CLI:

1. Explores your codebase and requirements
2. Identifies existing patterns and constraints
3. Drafts a step-by-step implementation plan
4. Presents the plan for your approval
5. Waits for feedback before writing any code

**When to use Plan Mode:**
- Starting a new project or major phase
- Complex features requiring architectural decisions
- When multiple valid approaches exist
- When you want to validate thinking before committing

**How to enter Plan Mode:**
```bash
> /plan
> Read the project specification and create an implementation plan 
> for the data warehouse layer
```

### Execution Mode: Build What Was Planned

Execution Mode is for **implementing approved plans**. The AI:

1. Reads progress files to understand current state
2. Identifies the next incomplete feature
3. Writes code, SQL, and configurations
4. Tests and validates the implementation
5. Updates progress files

**When to use Execution Mode:**
- After a plan is approved
- For well-defined, scoped tasks
- When continuing previous work

**How to use Execution Mode:**
```bash
> resume
```

Yes, it's that simple. Just say "resume" and Cortex Code CLI reads your progress files and continues where you left off.

### The Workflow in Practice

```
┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│   PLAN MODE      │     │   YOUR REVIEW     │     │ EXECUTION MODE   │
│                  │     │                   │     │                  │
│ "Here's my plan  │────▶│ "Looks good, but  │────▶│ "Implementing    │
│  to build the    │     │  let's also add   │     │  feature #23:    │
│  fact table..."  │     │  error handling"  │     │  Creating view..." │
└──────────────────┘     └───────────────────┘     └──────────────────┘
```

This separation ensures you're always in control. The AI proposes, you approve, then it executes.

---

## The Three Essential Files

The Long-Running Agent Pattern requires three files that work together:

### 1. Specification Document (`*_platform.md`)

This is your project's "constitution"—the source of truth for requirements, architecture, and the rules the AI must follow.

**Key sections:**
- How to execute the project (instructions for the AI)
- Long-running agent pattern rules
- Business requirements
- Technical requirements
- Feature breakdown by phase
- Validation checkpoints
- Success criteria

**Example excerpt:**
```markdown
# Sales Analytics Platform - Specification

## Critical Rules

1. **ONE FEATURE AT A TIME** - Never implement multiple features at once
2. **TEST EVERYTHING** - Features aren't done until verified
3. **DOCUMENT THOROUGHLY** - Next session has NO memory
4. **NEVER BREAK EXISTING** - Validate before adding new
5. **LEAVE CLEAN STATE** - No half-implemented code

## Feature Breakdown

### Phase 1: Infrastructure (Features 1-10)
- Create database
- Create schemas (RAW, STAGING, MARTS)
- Create warehouse
- Verify connectivity

### Phase 2: Data Layer (Features 11-20)
...
```

### 2. Feature List (`feature_list.json`)

This JSON file tracks every feature with its completion status. It's generated in Session 1 and updated throughout the project.

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
      "passes": true,
      "tested_at": "2024-01-15T10:30:00Z",
      "notes": "Created successfully"
    },
    {
      "id": 2,
      "phase": "infrastructure",
      "priority": 1,
      "title": "Create RAW schema",
      "passes": true,
      "tested_at": "2024-01-15T10:31:00Z",
      "notes": ""
    },
    {
      "id": 3,
      "phase": "infrastructure",
      "priority": 2,
      "title": "Create semantic model stage",
      "passes": false,
      "tested_at": null,
      "notes": ""
    }
  ]
}
```

**Key fields:**
- `priority`: 1 = must have, 2 = nice to have
- `passes`: Only `true` after successful testing
- `notes`: Implementation details for future reference

### 3. Progress Log (`cortex-progress.md`)

This Markdown file provides human-readable session history and current state.

```markdown
# Sales Analytics Platform - Progress Log

## Quick Status
- **Total Features**: 80
- **Completed**: 45
- **Remaining**: 35
- **Last Updated**: 2024-01-20T15:30:00Z

## Session History

### Session 5 - 2024-01-20
- **Type**: Mart Layer Implementation
- **Features Completed**: #31, #32, #33
- **Objects Created**: 
  - DYNAMIC TABLE: MARTS.FCT_ORDERS
  - DYNAMIC TABLE: MARTS.DAILY_SALES
- **Issues**: None
- **Next**: Implement feature #34 (SALES_BY_REGION table)

### Session 4 - 2024-01-19
- **Type**: Staging Layer
- **Features Completed**: #21, #22, #23, #24
...

## Current Snowflake Objects

| Type | Name | Schema | Status |
|------|------|--------|--------|
| DATABASE | SALES_ANALYTICS_DB | - | ✓ |
| SCHEMA | RAW | SALES_ANALYTICS_DB | ✓ |
| SCHEMA | STAGING | SALES_ANALYTICS_DB | ✓ |
| TABLE | ORDERS | RAW | ✓ (100K rows) |
| VIEW | STG_ORDERS | STAGING | ✓ |
| DYNAMIC TABLE | FCT_ORDERS | MARTS | ✓ |
```

---

## Real-World Example: Building a Sales Analytics Platform

Let me walk you through how I actually used this pattern to build a complete Sales Analytics Platform on Snowflake.

### The Project Scope

**Goal:** Build a self-service analytics platform for sales leaders with:
- Snowflake data warehouse (RAW → STAGING → MARTS)
- Dynamic Tables for real-time aggregation
- Semantic model for natural language queries (Cortex Analyst)
- Interactive Streamlit dashboard

**Scale:**
- 80 features across 9 phases
- 100,000 orders, 10,000 customers, 500 products
- 6 dashboard pages
- ~$394M in sample revenue data

### Session-by-Session Breakdown

#### Session 1: Foundation
```
Started: cortex
Command: /plan Read @sales_analytics_platform.md and execute this project

Results:
- Generated feature_list.json (80 features)
- Created cortex-progress.md
- Built database, schemas, warehouse
- Features completed: #1-#7
```

#### Sessions 2-3: Raw Data Layer
```
Command: resume

Results:
- Created 4 raw tables (ORDERS, CUSTOMERS, PRODUCTS, SALES_REPS)
- Generated 100K+ rows of realistic sample data
- Features completed: #11-#20
```

#### Sessions 4-5: Staging & Marts
```
Command: resume

Results:
- Created staging views with data quality flags
- Built FCT_ORDERS Dynamic Table joining all dimensions
- Created 5 aggregation Dynamic Tables
- All with 5-minute target lag
- Features completed: #21-#50
```

#### Session 6: Semantic Model
```
Command: resume

Results:
- Created sales_model.yaml (301 lines)
- Defined 15 dimensions, 12 measures, 5 time dimensions
- Tested with Cortex Analyst queries
- Features completed: #51-#60
```

#### Sessions 7-8: Streamlit Dashboard
```
Command: resume

Results:
- Built 6-page interactive dashboard
- Executive Dashboard, Regional Analysis, Product Analysis
- Sales Rep Leaderboard, Customer Insights, Cortex Analyst
- Added error handling, loading states, caching
- Features completed: #61-#77
```

#### Sessions 9-10: Polish & Bug Fixes
```
Command: resume

Results:
- Added drill-down capabilities
- Fixed SQL column naming issues
- Added documentation section
- Features completed: #78-#80 (partial)

Final status: 72/80 features (90%)
All Priority 1 features: 100% complete
```

### What Made This Work

1. **Clear specification upfront**: Every requirement documented before starting
2. **Strict one-feature-at-a-time rule**: Prevented half-done work
3. **Immediate progress updates**: Never lost track of state
4. **Validation at phase boundaries**: Caught issues early
5. **Priority system**: Delivered working product before enhancements

---

## How to Implement This Pattern in Your Projects

### Step 1: Create Your Specification Document

Start with a comprehensive specification that includes:

```markdown
# [Your Project] - Long-Running Project Specification

## How to Execute This Project

### Starting (First Session)
/plan
Read @[filename].md and execute this long-running project

### Continuing (Subsequent Sessions)
resume

---

# PART 1: LONG-RUNNING AGENT PATTERN

## Critical Rules
1. ONE FEATURE AT A TIME
2. TEST EVERYTHING
3. DOCUMENT THOROUGHLY
4. NEVER BREAK EXISTING
5. LEAVE CLEAN STATE

## Required Artifacts
- feature_list.json
- cortex-progress.md

---

# PART 2: PROJECT REQUIREMENTS

## Business Context
[What are you building and why?]

## Functional Requirements
[What must it do?]

## Technical Requirements
[How should it be built?]

## Feature Breakdown
[50-80 features organized by phase]

## Validation Checkpoints
[How to verify each phase works]

## Success Criteria
[Definition of done]
```

### Step 2: Start Your First Session

```bash
cortex

> /plan
> Read @my_project_platform.md and execute this long-running project 
> following the agent pattern defined in the document.
```

The AI will:
1. Analyze your specification
2. Generate `feature_list.json` with all features
3. Create `cortex-progress.md`
4. Begin implementing foundational features

### Step 3: Continue in Subsequent Sessions

```bash
cortex

> resume
```

That's it. The AI reads your progress files, validates existing work, and continues with the next incomplete feature.

### Step 4: Handle Edge Cases

**If context runs out mid-session:**
- Progress files are updated immediately
- Next session continues seamlessly

**If something breaks:**
- Set `passes: false` in feature_list.json
- Document the issue in notes
- Next session will fix it

**If requirements change:**
- Update the specification document
- Add new features to feature_list.json
- Continue with normal flow

---

## Best Practices I Learned

### Do This

| Practice | Why It Works |
|----------|--------------|
| ✅ Test before marking complete | Prevents false progress |
| ✅ Update progress immediately | Never lose state |
| ✅ Use P1/P2 priorities | Ship MVP, then enhance |
| ✅ Include validation queries | Catch regressions |
| ✅ Document blockers | Future sessions can address |

### Avoid This

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| ❌ Multiple features at once | Increases error risk |
| ❌ Skipping tests | Creates hidden debt |
| ❌ Batching progress updates | Risks losing work |
| ❌ Leaving broken state | Blocks next session |
| ❌ Deleting features | Loses audit trail |

---

## The Bigger Picture

The Long-Running Agent Pattern isn't just about building one project—it's about **changing how we work with AI**.

Instead of fighting context limitations, we embrace them. Instead of hoping the AI remembers, we ensure it has what it needs. Instead of one heroic session, we make sustainable progress.

This pattern works because it mirrors how humans actually work on complex projects:
- We take notes
- We track progress
- We validate our work
- We document for teammates (including future selves)

The AI becomes a true collaborator, not a tool you have to constantly re-educate.

---

## Try It Yourself

I've open-sourced the complete Sales Analytics Platform as a reference implementation:

**GitHub Repository:** [snowflake-cortex-code-long-running-agents](https://github.com/curious-bigcat/snowflake-cortex-code-long-running-agents)

**What's Included:**
- Complete specification document (template for your projects)
- Feature list with 80 tracked features
- Progress log showing 10 sessions of work
- All Snowflake SQL (DDL/DML)
- Semantic model for Cortex Analyst
- Full Streamlit application

**To get started:**
```bash
git clone https://github.com/curious-bigcat/snowflake-cortex-code-long-running-agents.git
cd snowflake-cortex-code-long-running-agents

# Use as a template
cp sales_analytics_platform.md my_project_platform.md

# Start building
cortex
> /plan
> Read @my_project_platform.md and execute this long-running project
```

---

## Conclusion

Building complex systems with AI doesn't have to mean fighting context limits. The Long-Running Agent Pattern provides a structured approach that:

- **Preserves context** across unlimited sessions
- **Tracks progress** with precision
- **Enables collaboration** between human and AI
- **Produces audit trails** for compliance and learning
- **Scales to any project size**

Whether you're building a data warehouse, an ML pipeline, a full-stack application, or any complex system, this pattern can transform how you work with AI assistants.

The future of software development isn't AI replacing developers—it's AI and developers working together more effectively. The Long-Running Agent Pattern is one step toward that future.

---

*What complex projects have you struggled to build with AI? I'd love to hear your experiences in the comments.*

---

### About the Author

This project was built using Snowflake's Cortex Code CLI, demonstrating how AI-assisted development can scale to production-grade systems. The complete code and documentation are available on GitHub for you to learn from, adapt, and improve.

---

**Tags:** `AI` `Snowflake` `Data Engineering` `Software Development` `Cortex` `LLM` `Productivity` `Tutorial`

---

*If you found this helpful, consider following for more content on AI-assisted development and data engineering.*
