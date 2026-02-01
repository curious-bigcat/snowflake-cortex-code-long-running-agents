# Adopting Anthropic's Long-Running Agents Pattern with Snowflake Cortex Code CLI

## A Practical Guide to Multi-Session AI Development for Complex Projects

*How to leverage Anthropic's agentic patterns through Snowflake's AI-powered CLI to build production systems that span multiple sessions*

---

## Introduction: The Evolution of AI Agents

Anthropic has been at the forefront of developing patterns for effective AI agent design. One of the most powerful concepts to emerge is the **Long-Running Agents pattern**—a methodology for breaking through the fundamental limitation of AI context windows to enable complex, multi-session projects.

Snowflake's **Cortex Code CLI** provides an ideal platform for implementing this pattern, combining Anthropic's Claude model with native Snowflake connectivity, file system access, and shell command execution. Together, they enable a new paradigm for AI-assisted software development.

This article explores:
- What Long-Running Agents are and why Anthropic developed this pattern
- How Cortex Code CLI implements agentic capabilities
- The Plan Mode and Execution Mode workflow
- Practical adoption strategies for your projects

---

## Part 1: Understanding Anthropic's Long-Running Agents Pattern

### The Context Window Challenge

Every large language model operates within a **context window**—the maximum amount of text it can process in a single conversation. For Claude, this is substantial (200K+ tokens), but for complex projects, it's still a limitation.

When building software, context accumulates rapidly:
- Requirements and specifications
- Code already written
- Debugging conversations
- Architecture decisions
- Test results and validations

Once context is exhausted, the model loses access to earlier information. Traditional approaches treat this as a hard boundary, limiting AI assistance to small, self-contained tasks.

### Anthropic's Solution: Externalized State

Anthropic's Long-Running Agents pattern addresses this through **externalized state management**. Instead of relying on the model's context window as the source of truth, the pattern prescribes:

1. **Persistent artifacts** that capture project state
2. **Structured progress tracking** across sessions
3. **Clear session protocols** for context restoration
4. **Atomic task completion** to prevent partial states

The key insight is that **the context window is temporary, but files are permanent**. By systematically writing state to files, an agent can maintain continuity across unlimited sessions.

### Core Principles from Anthropic's Research

The pattern embodies several principles from Anthropic's work on AI agents:

| Principle | Implementation |
|-----------|----------------|
| **Explicit over implicit** | All decisions documented in files |
| **Atomic operations** | One feature completed before starting next |
| **Verification loops** | Test before marking complete |
| **Graceful degradation** | Session can end at any point without data loss |
| **Human oversight** | Plan Mode enables approval before execution |

---

## Part 2: Cortex Code CLI - Anthropic's Claude for Snowflake

### What is Cortex Code CLI?

Cortex Code CLI is Snowflake's AI-powered command-line interface, built on **Anthropic's Claude** model. It's designed for software development workflows with deep integration into both local development environments and Snowflake's data platform.

```bash
# Start an interactive session
cortex

# You're now conversing with Claude, enhanced with tools
> Help me build a data pipeline for customer analytics
```

### Agentic Capabilities

What makes Cortex Code CLI an **agent** rather than just a chatbot is its ability to take actions:

| Capability | Description |
|------------|-------------|
| **SQL Execution** | Run queries directly against Snowflake |
| **File Operations** | Read, write, and edit files in your project |
| **Shell Commands** | Execute git, npm, python, and other CLI tools |
| **Web Access** | Fetch documentation and search for information |
| **Multi-step Reasoning** | Chain operations to accomplish complex goals |

These tools transform Claude from a conversational assistant into an agent that can **actually build things**.

### The Agent Loop

Cortex Code CLI implements what Anthropic calls the "agent loop":

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   User Request ──▶ Claude Reasoning ──▶ Tool Selection     │
│                           │                    │            │
│                           ▼                    ▼            │
│                    Tool Execution ◀──── Tool Results       │
│                           │                                 │
│                           ▼                                 │
│                    Continue or Respond                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

The model observes its environment, reasons about the next action, executes a tool, observes the result, and continues until the task is complete.

---

## Part 3: Plan Mode vs Execution Mode

Cortex Code CLI implements a critical concept for responsible AI agents: **separation of planning and execution**.

### Plan Mode: Think Before Acting

Plan Mode is entered with the `/plan` command. In this mode, the agent:

1. **Explores** the codebase and requirements
2. **Analyzes** existing patterns and constraints  
3. **Designs** a step-by-step implementation approach
4. **Presents** the plan for human approval
5. **Waits** for feedback before writing any code

```bash
> /plan
> I want to add authentication to my application

# Claude will:
# - Read your existing code
# - Research authentication patterns
# - Propose an implementation approach
# - Ask for your approval before proceeding
```

**Why Plan Mode matters:**
- Prevents the AI from charging ahead with wrong assumptions
- Enables human oversight of architectural decisions
- Reduces costly rework from misunderstood requirements
- Creates documentation of design rationale

### Execution Mode: Implement Approved Plans

Once a plan is approved, Execution Mode focuses on implementation:

```bash
> resume

# Claude will:
# - Read progress files to understand current state
# - Identify the next incomplete task
# - Implement with verification
# - Update progress tracking
```

The `resume` command is particularly powerful for long-running projects. It tells the agent to read externalized state and continue where it left off.

### The Workflow

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │
│  /plan      │────────▶│  Human      │────────▶│  resume     │
│  (Design)   │         │  Review     │         │  (Build)    │
│             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
      │                                               │
      │                                               │
      ▼                                               ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│              Externalized State (Files)                     │
│                                                             │
│   • specification.md    - Requirements & rules              │
│   • feature_list.json   - Progress tracking                 │
│   • cortex-progress.md  - Session history                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 4: Implementing the Long-Running Agents Pattern

### The Three Essential Artifacts

To adopt Anthropic's pattern with Cortex Code CLI, you need three files:

#### 1. Specification Document

This is your project's constitution—the persistent source of truth that survives across all sessions.

```markdown
# [Project Name] - Long-Running Agent Specification

## Execution Protocol

### First Session
/plan
Read @[this_file].md and execute this long-running project

### Subsequent Sessions
resume

## Agent Rules
1. ONE TASK AT A TIME - Complete before starting next
2. VERIFY EVERYTHING - Test before marking done
3. UPDATE IMMEDIATELY - Never batch progress updates
4. PRESERVE STATE - Files are the source of truth
5. DOCUMENT DECISIONS - Future sessions need context

## Project Requirements
[Your specific requirements here]

## Feature Breakdown
[Numbered list of all features to build]
```

#### 2. Feature List (JSON)

Machine-readable progress tracking:

```json
{
  "project": "Project Name",
  "total_features": 50,
  "features": [
    {
      "id": 1,
      "title": "Feature description",
      "passes": true,
      "tested_at": "2024-01-15T10:30:00Z",
      "notes": "Implementation details"
    }
  ]
}
```

#### 3. Progress Log (Markdown)

Human-readable session history:

```markdown
# Progress Log

## Current Status
- Completed: 25/50 features
- Current Phase: Phase 3

## Session History

### Session 4 - 2024-01-18
- Completed: Features #20-25
- Created: API endpoints
- Next: Frontend integration
```

### Session Protocol

**Starting a new project:**
```bash
cortex
> /plan
> Read @my_project.md and execute this long-running project 
> following the agent pattern defined in the document
```

The agent will:
1. Parse your specification
2. Generate `feature_list.json`
3. Create `cortex-progress.md`
4. Begin implementing features
5. Update progress after each completion

**Continuing an existing project:**
```bash
cortex
> resume
```

The agent will:
1. Read `feature_list.json` and `cortex-progress.md`
2. Identify current state and next task
3. Validate existing work still functions
4. Continue implementation
5. Update progress files

---

## Part 5: Why This Pattern Works

### Alignment with Anthropic's Agent Design Principles

The Long-Running Agents pattern aligns with several key principles from Anthropic's research:

**1. Transparency**
All decisions, progress, and state are written to files. There's no hidden state in the model's "memory"—everything is inspectable.

**2. Human Control**
Plan Mode ensures humans approve major decisions. The agent proposes, the human disposes.

**3. Graceful Failure**
If a session ends unexpectedly, progress files capture the last known good state. Nothing is lost.

**4. Bounded Autonomy**
The agent operates within clear constraints defined in the specification. It knows what it should and shouldn't do.

### Comparison to Traditional Approaches

| Aspect | Traditional AI Chat | Long-Running Agents |
|--------|---------------------|---------------------|
| Context | Limited to session | Unlimited via files |
| State | Lost on session end | Persisted permanently |
| Progress | Manual tracking | Automatic tracking |
| Oversight | Post-hoc review | Plan Mode approval |
| Complexity | Small tasks only | Arbitrarily complex |

---

## Part 6: Practical Example - Sales Analytics Platform

To illustrate the pattern in practice, I built a complete Sales Analytics Platform on Snowflake across 10 sessions.

### Project Scope
- 80 features across 9 phases
- Snowflake data warehouse (RAW → STAGING → MARTS)
- Dynamic Tables for real-time aggregation
- Semantic model for Cortex Analyst
- Interactive Streamlit dashboard

### How the Pattern Enabled This

**Without the pattern:** This project would require maintaining context about:
- Database schema decisions from Session 1
- Data model choices from Session 3
- API patterns established in Session 5
- ...all available in Session 10

Impossible with a traditional context window.

**With the pattern:** Each session reads progress files and has complete context:

```
Session 10:
> resume

Claude reads:
- feature_list.json (72/80 complete)
- cortex-progress.md (full history)
- Validates: FCT_ORDERS exists with 100K rows
- Continues: Feature #73 - Dashboard drill-down
```

### Results

| Metric | Value |
|--------|-------|
| Total Sessions | 10 |
| Features Completed | 72/80 (90%) |
| Priority 1 Features | 100% |
| Context Lost | 0% |
| Rework Required | Minimal |

The complete implementation is available on GitHub as a reference for adopting this pattern.

---

## Part 7: Adopting the Pattern for Your Projects

### Step 1: Define Your Specification

Create a comprehensive specification document that includes:
- Execution protocol (how to start/continue)
- Agent rules (constraints and guidelines)
- Feature breakdown (everything to build)
- Validation criteria (how to verify)

### Step 2: Start with Plan Mode

```bash
cortex
> /plan
> Read @specification.md and execute this project
```

Let the agent generate the initial feature list and progress tracking.

### Step 3: Iterate with Resume

```bash
cortex
> resume
```

Each session picks up where the last left off. The agent maintains continuity automatically.

### Step 4: Review and Adjust

- Check `feature_list.json` for progress
- Review `cortex-progress.md` for history
- Update specification if requirements change
- Add features to the list as needed

### Best Practices

| Do | Don't |
|----|-------|
| ✅ Keep specification updated | ❌ Let it drift from reality |
| ✅ Verify before marking complete | ❌ Assume tests passed |
| ✅ Document blockers immediately | ❌ Leave issues undocumented |
| ✅ Use priorities (P1/P2) | ❌ Treat all features equally |
| ✅ End sessions cleanly | ❌ Stop mid-feature |

---

## Conclusion: The Future of AI-Assisted Development

Anthropic's Long-Running Agents pattern represents a significant evolution in how we work with AI. By externalizing state to files and implementing clear protocols for session continuity, we can:

- **Build arbitrarily complex systems** with AI assistance
- **Maintain perfect context** across unlimited sessions
- **Preserve human oversight** through Plan Mode
- **Create auditable trails** of all decisions

Snowflake's Cortex Code CLI provides an excellent platform for adopting this pattern, combining Claude's reasoning capabilities with practical tools for software development.

The era of AI being limited to small, isolated tasks is ending. With the right patterns and tools, AI agents can be true partners in building production systems.

---

## Resources

**GitHub Repository:** [snowflake-cortex-code-long-running-agents](https://github.com/curious-bigcat/snowflake-cortex-code-long-running-agents)

Contains:
- Complete specification template
- Feature list and progress tracking examples
- Reference implementation (Sales Analytics Platform)
- All SQL, Python, and configuration files

**Further Reading:**
- [Anthropic's Research on AI Agents](https://www.anthropic.com)
- [Snowflake Cortex Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex)
- [Claude Model Card](https://www.anthropic.com/claude)

---

*This article demonstrates how adopting established patterns from AI research can dramatically expand what's possible with AI-assisted development. The Long-Running Agents pattern isn't just theoretical—it's practical, proven, and ready for your next complex project.*

---

**Tags:** `Anthropic` `Claude` `AI Agents` `Snowflake` `Cortex Code` `Long-Running Agents` `Software Development` `LLM Patterns`
