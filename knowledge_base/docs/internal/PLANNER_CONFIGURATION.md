---
original_file: "PLANNER_CONFIGURATION"
processed_date: 2026-01-31T18:08:26.485339
type: document_extraction
---

# Document Extraction: PLANNER_CONFIGURATION

# Charter & Stone Planner Configuration
## Project Management Source of Truth

**Plan Name:** Launch Operations  
**Plan ID:** `y9DwHD-ObEGDHvjmhIFtW2UAAnJj`  
**Last Export:** January 31, 2026  
**Total Tasks:** 82

---

## Purpose

This document defines the authoritative configuration for Charter & Stone's Microsoft Planner instance. It serves as the source of truth for:

1. Bucket definitions and their purposes
2. Task naming conventions and templates
3. Priority and label taxonomies
4. Assignment protocols
5. Automation integration points

**Governance Principle:** When there is conflict between Planner state and this document, escalate to Aaron and Amanda for executive decision. This document represents intended state; Planner represents actual state.

---

## Bucket Definitions

### Active Buckets

| Bucket Name | Purpose | Owner | Automation Integration |
|-------------|---------|-------|----------------------|
| **Digital Teammates Org Chart (R&D)** | Agent development, infrastructure, technical sprints | Aaron | Power Automate creates tasks here for tech work |
| **Strategy & Intel** | University signals, prospect research, market intelligence | Aaron | Watchdog signals land here via Power Automate |
| **Legal & Structure** | LLC formation, operating agreement, compliance | Aaron | None (manual) |
| **Financial Infrastructure** | Banking, accounting, payment processing | Aaron | None (manual) |
| **Branding & Assets** | Logo, website, marketing materials | Aaron | None (manual) |
| **Operations Blueprint** | SOPs, playbooks, org chart | Amanda | None (manual) |
| **Sandbox/Parking Lot** | Deferred items, experiments, future ideas | Both | None (manual) |
| **Watchdog Inbox** | Raw signals awaiting triage | System | Watchdog deposits here; Orchestrator processes |

### Bucket Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Watchdog Inbox │────▶│  Strategy &     │────▶│  Completed      │
│  (Auto-created) │     │  Intel (Triage) │     │  (Archived)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │
         │                      ▼
         │              ┌─────────────────┐
         │              │  Digital        │
         │              │  Teammates R&D  │
         │              │  (If tech work) │
         │              └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR FLOW                            │
│  1. Parse signal type (DISTRESS/FORECAST)                       │
│  2. Enrich with IRS 990 data (if applicable)                    │
│  3. Set priority based on severity                              │
│  4. Move to Strategy & Intel for human review                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Task Naming Conventions

### Signal Tasks (Auto-Generated)

Format: `[SIGNAL_TYPE] Institution Name - Headline...`

| Signal Type | Icon | Meaning | Auto-Priority |
|-------------|------|---------|---------------|
| `[🔴 DISTRESS]` | Red Circle | Financial crisis, layoffs, closures, no-confidence votes | Urgent |
| `[🟢 FORECAST]` | Green Circle | Master plans, expansions, positive news | Important |
| `[🟡 WATCH]` | Yellow Circle | Emerging situation, needs monitoring | Medium |
| `[⚪ INFO]` | White Circle | General intelligence, no action needed | Low |

**Examples:**
- `[🔴 DISTRESS] West Virginia University - Board approves cuts to degree programs`
- `[🟢 FORECAST] NAU $2 Billion Master Plan Approved`
- `[🟡 WATCH] Baker College restructuring continues`

### Sprint Tasks (Manual)

Format: `Sprint N: Component Name - Objective`

**Examples:**
- `Sprint 2: The Orchestrator - Automated Signal Routing`
- `Sprint 3: Distress Signal Triage & Deep Dive Prioritization`

### Feature Tasks (Manual)

Format: `Feature: Component - Capability Description`

**Examples:**
- `Feature: Teams Channel Segmentation Logic`
- `Feature: Planner-to-Teams Notification Stream`

### Product Tasks (Manual)

Format: `Product: "Agent Name" (Description)`

**Examples:**
- `Product: The 'Oracle' (Conversational Intelligence Engine)`
- `Product: The "Mirror" (Client Demo Agent)`

---

## Priority Taxonomy

| Priority | When to Use | SLA |
|----------|-------------|-----|
| **Urgent** | Blocking other work; revenue-impacting; time-sensitive signals | 24-48 hours |
| **Important** | Critical path items; high-value prospects; infrastructure | 1 week |
| **Medium** | Standard work; normal pipeline items | 2 weeks |
| **Low** | Nice-to-have; exploratory; can be deferred | No SLA |

### Priority Assignment Rules

**Automated (via Power Automate):**
- `[🔴 DISTRESS]` signals → Urgent
- `[🟢 FORECAST]` signals → Important
- `[🟡 WATCH]` signals → Medium
- `[⚪ INFO]` signals → Low

**Manual Override Triggers:**
- Geographic proximity (TX/OH) → Increase one level
- Enrollment >10,000 → Increase one level
- Budget deficit >$50M → Increase one level
- Leadership crisis + financial crisis → Urgent regardless of signal type

---

## Assignment Protocol

### Default Assignments

| Bucket | Default Assignee |
|--------|------------------|
| Digital Teammates Org Chart (R&D) | Aaron Shirley |
| Strategy & Intel | Aaron Shirley |
| Legal & Structure | Aaron Shirley |
| Financial Infrastructure | Aaron Shirley |
| Branding & Assets | Aaron Shirley |
| Operations Blueprint | Amanda Keeton |
| Sandbox/Parking Lot | Unassigned |
| Watchdog Inbox | Unassigned (system-generated) |

### User IDs (For Automation)

| User | Graph API User ID |
|------|-------------------|
| Aaron Shirley | `b0c032d0-5d31-48e1-8263-5cc817aa63e9` |
| Amanda Keeton | (To be documented) |

---

## Task Description Templates

### Signal Task Template

```markdown
Triggered by Watchdog V2.2.
Type: [SIGNAL_TYPE]
Keyword: [triggering_keyword]
Source: [news_url]

🤖 Automated Deep Dive:
Organization: [org_name]
Tax Year: [year]
Revenue: $[amount]
Net Assets: $[amount]
Link: [990_pdf_url]

---
**Human Review Required:**
- [ ] Verify signal accuracy
- [ ] Assess geographic fit
- [ ] Evaluate engagement potential
- [ ] Decide: Pursue / Monitor / Archive
```

### Sprint Task Template

```markdown
## Objective
[One-sentence goal]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Approach
[Brief architecture or implementation notes]

## Dependencies
- Depends on: [task_id or "None"]
- Blocks: [task_id or "None"]

## Time Estimate
[X hours/days]

## Execution Log
[Date] - [Status update]
```

### Digital Teammate Definition Template

```markdown
**Role:** [Job title analogy]
**Status:** [Conceptual | In Development | Beta | Production]
**Priority Tier:** [1-Revenue Enabler | 2-Quality | 3-Growth]

## Job Description
[2-3 sentences describing what this agent does]

## Inputs
- [Input 1]
- [Input 2]

## Outputs
- [Output 1]
- [Output 2]

## Dependencies
- Requires: [Other agents or systems]
- Feeds into: [Downstream agents]

## Technical Notes
[Implementation details, API references, etc.]
```

---

## Automation Integration Points

### Power Automate Triggers (Automated — Unattended)

| Trigger | Source | Destination |
|---------|--------|-------------|
| File created in "Incoming Signals" | OneDrive (rclone sync) | Create task in Watchdog Inbox |
| Task completed | Any bucket | Post summary to Teams |

### Claude Desktop MCP Tools (Interactive — Session-Based)

**All Planner operations available during active Claude sessions:**

| Operation | MCP Tool | Example Prompt |
|-----------|----------|----------------|
| List tasks | `list_tasks` | "What's in Strategy & Intel?" |
| Get details | `get_task_details` | "Show me the WVU distress task details" |
| Create task | `create_task` | "Create a task to follow up with Baker College" |
| Update task | `update_task` | "Change that task's priority to Urgent" |
| Complete task | `complete_task` | "Mark the Oracle Phase 1 task complete" |
| Move task | `move_task` | "Move this to Sandbox" |

**Why Both Systems?**
- **Power Automate:** Handles automated signal pipeline 24/7 without supervision
- **Claude MCP:** Enables Aaron to manage tasks conversationally during work sessions

### Prohibited Automated Actions

The following actions must NOT be automated without human approval:

1. **Delete tasks** — Archive to Sandbox instead
2. **Change assignments** — Notify both parties first
3. **Modify completed tasks** — Preserves audit trail
4. **Create tasks in Legal/Financial buckets** — Sensitive; manual only

---

## Governance Procedures

### Weekly Audit (Aaron)

Every Monday, review:
- [ ] Tasks overdue >7 days — Escalate or re-prioritize
- [ ] Watchdog Inbox depth — Should be <10 items
- [ ] Unassigned tasks — Assign or move to Sandbox

### Monthly Reconciliation (Aaron + Amanda)

First of each month:
- [ ] Compare Planner state to this document
- [ ] Identify drift (buckets renamed, conventions violated)
- [ ] Update this document OR fix Planner
- [ ] Review Deprecation Log for superseded tasks

### Drift Detection Queries

Ask Claude to run these checks:

1. "List all tasks without assignees that aren't in Sandbox"
2. "List all tasks overdue by more than 14 days"
3. "List all tasks in Strategy & Intel that don't follow signal naming convention"
4. "Count tasks per bucket and compare to last month"

---

## Current State Summary (as of Jan 31, 2026)

| Bucket | Task Count | Overdue |
|--------|------------|---------|
| Digital Teammates Org Chart (R&D) | 24 | 0 |
| Strategy & Intel | 34 | 21 |
| Legal & Structure | 6 | 3 |
| Financial Infrastructure | 7 | 0 |
| Branding & Assets | 4 | 2 |
| Operations Blueprint | 2 | 0 |
| Sandbox/Parking Lot | 2 | 0 |
| Watchdog Inbox | 3 | 0 |

**Note:** Strategy & Intel overdue count reflects auto-generated signal tasks that have not been triaged. This is expected behavior during architecture pivot.

---

## Appendix: Bucket ID Reference

For Power Automate flow configuration:

| Bucket Name | Bucket ID |
|-------------|-----------|
| (To be populated after Power Automate setup) | |

---

*Document Version: 1.0*  
*Last Updated: January 31, 2026*  
*Owner: Aaron Shirley (CSO)*  
*Review Frequency: Monthly*

