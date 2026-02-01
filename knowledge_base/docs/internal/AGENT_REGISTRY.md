---
original_file: "AGENT_REGISTRY"
processed_date: 2026-01-31T18:09:04.430777
type: document_extraction
---

# Document Extraction: AGENT_REGISTRY

# Charter & Stone Agent Registry
## Digital Teammates Catalog

**Purpose:** Authoritative inventory of all AI agents in development or production. Defines roles, dependencies, priority tiers, and current status.

**Last Updated:** January 31, 2026  
**Total Agents:** 12  
**Production:** 3 | In Development: 1 | Planned: 8

---

## Priority Tier Framework

| Tier | Category | Business Rationale | Timeline |
|------|----------|-------------------|----------|
| **Tier 1** | Revenue Enablers | Directly generates leads or closes deals | Q1 2026 |
| **Tier 2** | Quality & Coordination | Ensures accuracy, prevents errors, orchestrates workflows | Q2 2026 |
| **Tier 3** | Growth Accelerators | Scales operations, automates marketing, optimizes pricing | Q3-Q4 2026 |

---

## Production Agents

### The Watchdog
**Codename:** `watchdog`  
**Role:** Intelligence Officer  
**Tier:** 1 — Revenue Enabler  
**Status:** ✅ PRODUCTION (v2.2)

**Description:**  
Monitors RSS feeds, news sources, and educational publications for signals indicating university distress or opportunity. Filters by keywords and publishes alerts.

**Location:** Raspberry Pi (Sentinel)  
**Schedule:** Hourly via systemd

**Inputs:**
- Google News RSS feeds
- Higher Ed news sources
- Keyword watchlist (DISTRESS: layoffs, deficit, closure, resigns, no-confidence; FORECAST: master plan, expansion, approved)

**Outputs:**
- Signal files in `knowledge_base/signals/`
- Synced to SharePoint via rclone
- Triggers Power Automate → Planner task

**Dependencies:**
- ProPublica API (IRS 990 enrichment)
- rclone sync to SharePoint
- Power Automate flow

**Key Metrics:**
- Signals detected per day: ~5-15
- False positive rate: <10% (target)
- Age filter: Articles <30 days

---

### The Oracle
**Codename:** `oracle`  
**Role:** Conversational Intelligence Engine  
**Tier:** 1 — Revenue Enabler  
**Status:** ✅ PRODUCTION (v2.1 "The Bridge")

**Description:**  
Retrieval-Augmented Generation (RAG) system that allows Claude to search the accumulated knowledge base via natural language queries.

**Location:** MCP Server (Windows) + Pi (filesystem)  
**Activation:** On-demand via Claude Desktop

**Inputs:**
- User queries via Claude Desktop
- Knowledge base directory structure

**Outputs:**
- Search results with file paths
- Content snippets for synthesis

**Dependencies:**
- SSH connection to Pi
- Knowledge base populated by Watchdog/Sentinel

**Phases:**
- ✅ Phase 1: Memory (Data Ingestion) — COMPLETE
- ✅ Phase 2: The Bridge (MCP Tooling) — COMPLETE
- ⏸️ Phase 3: The Face (Web Interface) — DEFERRED

---

### The Orchestrator
**Codename:** `orchestrator`  
**Role:** Signal Router / Enrichment Engine  
**Tier:** 2 — Quality & Coordination  
**Status:** ✅ PRODUCTION (v2.4)

**Description:**  
Processes raw signals from Watchdog, enriches them with IRS 990 financial data, and routes them to appropriate Planner buckets.

**Location:** Raspberry Pi (Sentinel)  
**Schedule:** Every 15 minutes via systemd

**Inputs:**
- Signal files from `knowledge_base/signals/`
- ProPublica Nonprofit Explorer API

**Outputs:**
- Enriched signal files with financial data
- Files moved to `knowledge_base/processed/`

**Dependencies:**
- Watchdog (upstream)
- ProPublica API access
- Power Automate (downstream for task creation)

**Key Capabilities:**
- Parses YAML frontmatter from signal files
- Maps severity to Planner priority
- Appends IRS 990 data (Revenue, Net Assets, PDF link)

---

## In Development

### The Mirror
**Codename:** `mirror`  
**Role:** Client Demo Agent / Show & Tell Specialist  
**Tier:** 1 — Revenue Enabler  
**Status:** 🔄 IN DEVELOPMENT

**Description:**  
Sandboxed chatbot for demonstrating AI capabilities to prospective university clients. Allows prospects to upload their own documents and query them in real-time.

**Target Completion:** February 28, 2026

**Value Proposition:**  
"Upload your Student Handbook and ask it questions right now." Demonstrates time-savings viscerally in first meeting.

**Technical Approach:**
- Streamlit or Chainlit web interface
- Hosted on Pi or Azure (TBD)
- Secure auth required
- Document isolation per session

**Dependencies:**
- Oracle (core RAG capability)
- Web hosting infrastructure

---

## Planned Agents (Priority Order)

### The Outreach Architect
**Codename:** `outreach`  
**Role:** Sales Development Rep (SDR)  
**Tier:** 1 — Revenue Enabler  
**Status:** 📋 PLANNED  
**Target:** March 14, 2026

**Description:**  
Ingests dossiers from analysis and drafts cold outreach emails. Produces 3 variations for human review.

**Inputs:** University dossiers, contact information  
**Outputs:** Draft emails in "Review" folder  
**Dependencies:** Oracle, Deep Dive analysis complete

---

### The Field Marshal
**Codename:** `field_marshal`  
**Role:** Chief Compliance & Quality Officer  
**Tier:** 2 — Quality & Coordination  
**Status:** 📋 PLANNED  
**Target:** March 31, 2026

**Description:**  
Gatekeeper agent. Nothing leaves the building without sign-off. Fact-checks stats, ensures tone matches brand voice, can kill processes that fail audit.

**Inputs:** Draft outputs from all agents  
**Outputs:** Approved/Rejected with feedback  
**Dependencies:** All Tier 1 agents operational

---

### The Floor General
**Codename:** `floor_general`  
**Role:** Operations Manager / Router  
**Tier:** 2 — Quality & Coordination  
**Status:** 📋 PLANNED  
**Target:** April 14, 2026

**Description:**  
Prevents agents from working in silos. When Political Officer sees a new bill, Floor General wakes up Analyst, then triggers Broadcaster.

**Inputs:** Events from all agents  
**Outputs:** Orchestration commands  
**Dependencies:** Multiple agents operational

---

### The Mechanic
**Codename:** `mechanic`  
**Role:** Site Reliability Engineer (SRE)  
**Tier:** 2 — Quality & Coordination  
**Status:** 📋 PLANNED  
**Target:** April 30, 2026

**Description:**  
Infrastructure health monitoring. Dead man's switch, resource monitoring, self-healing for hung services.

**Phases:**
- Phase 1: Alerting (SMS/Teams if daemon doesn't check in)
- Phase 2: Dashboard (SharePoint status page)
- Phase 3: Recommendations (auto-generate optimization tasks)

---

### The Broadcaster
**Codename:** `broadcaster`  
**Role:** CMO / Marketing Director  
**Tier:** 3 — Growth Accelerator  
**Status:** 📋 PLANNED  
**Target:** May 14, 2026

**Description:**  
Content engine. Auto-drafts LinkedIn posts from Policy Impact Briefs. Scans analytics weekly. Produces Growth Reports.

---

### The Political Officer
**Codename:** `political_officer`  
**Role:** Government Relations Specialist  
**Tier:** 3 — Growth Accelerator  
**Status:** 📋 PLANNED  
**Target:** May 31, 2026

**Description:**  
Monitors state legislatures, THECB meeting minutes, federal DOE briefings. Tracks lobbyist activity. Produces Policy Impact Briefs.

---

### The CFO Bot
**Codename:** `cfo_bot`  
**Role:** Revenue Strategy Lead  
**Tier:** 3 — Growth Accelerator  
**Status:** 📋 PLANNED  
**Target:** December 31, 2026 (deferred)

**Description:**  
Dynamic pricing analysis. Scenario planning on university budgets. Recommends fee structures based on value delivered.

---

### The Deep Dive Analyst
**Codename:** `deep_dive`  
**Role:** Junior Analyst  
**Tier:** 1 — Revenue Enabler  
**Status:** ✅ COMPLETE (Manual via Claude)

**Description:**  
Takes university name, autonomously reads IRS 990s and strategic plans, generates 1-page dossier.

**Note:** Currently performed manually via Claude Desktop with Oracle search. Future: Automated pipeline from signal → dossier.

---

## Dependency Graph

```
                    ┌─────────────┐
                    │  Watchdog   │
                    │  (Signals)  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Orchestrator│
                    │ (Enrichment)│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Oracle  │ │Deep Dive │ │ Planner  │
        │ (Search) │ │(Analysis)│ │ (Tasks)  │
        └────┬─────┘ └────┬─────┘ └──────────┘
             │            │
             └─────┬──────┘
                   │
                   ▼
             ┌──────────┐
             │  Mirror  │
             │  (Demo)  │
             └────┬─────┘
                  │
                  ▼
             ┌──────────┐      ┌──────────────┐
             │ Outreach │─────▶│ Field Marshal│
             │ (Emails) │      │  (QA Gate)   │
             └──────────┘      └──────────────┘
```

---

## Agent Development Protocol

When building a new agent:

1. **Define in this registry** — Role, tier, dependencies, inputs/outputs
2. **Create Planner task** — Use "Product:" naming convention
3. **Build in isolation** — Ensure it works standalone before integration
4. **Document in OPERATIONS_MANUAL.md** — Deployment steps, configuration
5. **Test with Field Marshal** — Once available, all outputs must pass QA
6. **Update this registry** — Move from Planned → In Development → Production

---

## Decommissioned Agents

| Agent | Reason | Date | Notes |
|-------|--------|------|-------|
| Planner MCP (Write) | Architecture V3 Pivot | 2026-01-31 | Replaced by Power Automate |

---

*Document Version: 1.0*  
*Last Updated: January 31, 2026*  
*Owner: Aaron Shirley (CSO)*

