---
original_file: "DEPRECATION_LOG"
processed_date: 2026-01-31T18:08:39.250590
type: document_extraction
---

# Document Extraction: DEPRECATION_LOG

# Charter & Stone Deprecation Log
## Infrastructure Decisions Archive

**Purpose:** This document records all deprecated systems, tools, and approaches. It serves as institutional memory to prevent re-solving solved problems and to provide context for future architectural decisions.

---

## Deprecation Entry #001

**Date:** January 31, 2026  
**Component:** Planner MCP Server — DAEMON/AUTOMATED Write Operations  
**Status:** DEPRECATED FOR AUTOMATION ONLY  
**Replacement:** Microsoft Power Automate (for automated signal → task pipeline)

### What Was Deprecated

Using Planner MCP write tools as part of **unattended automated workflows** (daemons, background scripts).

**NOT deprecated:** Using these same tools during **interactive Claude sessions** with Aaron present.

### Tools Status

| Tool | Automated/Daemon Use | Interactive Session Use |
|------|---------------------|------------------------|
| `create_task` | ❌ DEPRECATED | ✅ ACTIVE |
| `update_task` | ❌ DEPRECATED | ✅ ACTIVE |
| `complete_task` | ❌ DEPRECATED | ✅ ACTIVE |
| `move_task` | ❌ DEPRECATED | ✅ ACTIVE |
| `add_checklist_item` | ❌ DEPRECATED | ✅ ACTIVE |
| `list_tasks` | ✅ ACTIVE | ✅ ACTIVE |
| `get_task_details` | ✅ ACTIVE | ✅ ACTIVE |
| `search_oracle` | ✅ ACTIVE | ✅ ACTIVE |

### Why This Distinction Matters

**Automated/Daemon Use (DEPRECATED):**
- Runs 24/7 without human supervision
- Failures are silent — signals could be lost
- SSH connection must persist through Windows sleep cycles
- Token refresh must happen automatically
- No one watching to restart if it breaks

**Interactive Session Use (ACTIVE):**
- Aaron is present and engaged with Claude
- Failures are immediately visible
- Can restart MCP server if needed
- Can fall back to manual Planner UI
- "Good enough" reliability is acceptable

### Why Deprecated

**Root Cause Analysis:**

The Planner MCP write operations experienced systemic reliability failures when used as a background daemon:

1. **SSH Connection Fragility**
   - Windows sleep/wake cycles broke SSH connections to the Raspberry Pi
   - Paramiko library did not handle reconnection gracefully
   - Result: "Tool not found" errors after laptop sleep

2. **Token Refresh Race Conditions**
   - MSAL token refresh competed with active API calls
   - Tokens cached in `~/.planner_mcp_token_cache.json` became stale
   - Result: 401 Unauthorized errors requiring manual re-authentication

3. **Zombie Process Accumulation**
   - Failed MCP server instances did not terminate cleanly
   - Multiple Python processes accumulated, blocking port bindings
   - Result: Required manual `taskkill /IM python.exe /F`

4. **Cascading Tool Registration Failures**
   - Single tool failure during registration caused all tools to fail
   - No defensive isolation between tool registrations
   - Result: Complete MCP server unavailability

**Strategic Assessment:**

Two independent AI systems (Claude and Gemini) conducted adversarial review and concluded:

> "You are writing custom code to move a text string from a file to a to-do list. That is not a competitive advantage; it's plumbing." — Gemini

> "You're spending 70% of your engineering cycles on commodity plumbing and 30% on actual differentiation." — Claude

The write operations were "undifferentiated heavy lifting" — functionality that Microsoft Power Automate provides natively with enterprise reliability.

### Alternative Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| Continue debugging MCP | Preserves existing code | 40+ hours hardening work; still fragile | REJECTED |
| Azure Functions | Enterprise-grade reliability | Learning curve; timeout limits; cloud IP blocking | DEFERRED |
| Power Automate | Zero-code; 24/7 uptime; native M365 | Less flexibility; no programmatic writes from Claude | SELECTED |

### Migration Path

**Old Workflow:**
```
Watchdog (Pi) → SSH → Windows → MCP Server → Graph API → Planner
```

**New Workflow:**
```
Watchdog (Pi) → rclone → SharePoint → Power Automate → Planner
```

### Files Affected

| File | Action |
|------|--------|
| `C:\Users\tasms\CharterStone\PlannerMCP\server.py` | Archive; do not delete |
| `~/.planner_mcp_token_cache.json` | Retain for read operations |
| `claude_desktop_config.json` | Update to remove write tools |

### Lessons Learned

1. **Validate reliability requirements before building.** The write operations needed daemon-level reliability (24/7, unattended). This was not achievable with the SSH + Windows + Python + MSAL stack.

2. **Separate automation from analysis.** Background processes need enterprise infrastructure. Interactive tools can tolerate occasional restarts.

3. **Don't build what Microsoft maintains.** Power Automate has thousands of engineers ensuring uptime. We have two people.

4. **Sunk cost is real but recoverable.** The code wasn't wasted — it validated the workflow and informed the Power Automate design.

---

## Deprecation Entry #002

**Date:** January 31, 2026  
**Component:** SSH-Based Data Transport for Automation  
**Status:** DEPRECATED  
**Replacement:** rclone sync to SharePoint/OneDrive

### What Was Deprecated

Using SSH tunnels from Windows to Raspberry Pi as the primary data transport layer for automated workflows.

### Why Deprecated

1. **Single point of failure:** Windows laptop must be awake and connected
2. **Network dependency:** IP changes, SSH key rotations, firewall rules all break connectivity
3. **No offline tolerance:** If laptop is unavailable, entire pipeline halts

### What Was Retained

SSH remains available for:
- Interactive Oracle searches (on-demand, not daemon)
- Manual Pi administration
- Debugging and development

### Replacement Architecture

```
Pi filesystem → rclone → OneDrive/SharePoint → Power Automate
```

**Benefits:**
- Pi can operate independently of Windows machine
- SharePoint provides 99.9% uptime SLA
- Power Automate triggers regardless of laptop state

---

## Deprecation Entry #003

**Date:** January 31, 2026  
**Component:** Planner Task `KNxIw9nm5EWWoIYV1NCeVWUABI3K` — MCP Server Stability Fix  
**Status:** SUPERSEDED  
**Replacement:** Architecture V3 Pivot

### What Was Deprecated

A 7-phase hardening plan for the MCP server that included:
- SSH connection pooling with auto-reconnect
- Heartbeat mechanism for self-monitoring
- Defensive tool registration
- Windows Service integration

### Why Superseded

The architectural pivot eliminates the need for this hardening:

- SSH reliability no longer matters for automation (rclone handles sync)
- Daemon-level uptime no longer required (Power Automate handles triggers)
- Defensive registration unnecessary (read-only tools are simpler)

**Estimated time saved:** 40+ hours of development work

### Action Required

- Archive task in Planner with note: "Superseded by Architecture V3 Pivot — see DEPRECATION_LOG.md"
- Do not delete — preserves institutional memory of the problem diagnosis

## Deprecation Entry #004

**Date:** January 31, 2026  
**Component:** Charter & Stone HQ — Team / SharePoint Site  
**Status:** DEPRECATED  
**Replacement:** Unified "Charter & Stone" Team / SharePoint Site

### What Was Deprecated

The separate "Charter & Stone HQ" Microsoft Team and associated SharePoint site.

### Why Deprecated

- Fragmented document storage across multiple sites
- Confusion about which site contains authoritative documents
- Unnecessary complexity for two-person team

### Migration Path

All content from "Charter & Stone HQ" consolidates to the unified "Charter & Stone" Team SharePoint:

```
Charter & Stone/
├── Documents/
│   ├── Operations/         # System documentation
│   ├── Governance/         # Project management SOT
│   ├── Technical/          # MCP, Power Automate docs
│   └── Intelligence/       # Signal taxonomy, prospect criteria
```

### Action Required

1. Move all documents from HQ site to unified site
2. Update any rclone configurations pointing to HQ site
3. Update any Power Automate flows referencing HQ site
4. Delete or archive HQ team once migration verified

---

## Future Deprecation Candidates

| Component | Trigger | Replacement |
|-----------|---------|-------------|
| Raspberry Pi (Watchdog) | Hardware failure OR >2 hrs/week maintenance | Azure Functions |
| Oracle MCP (SSH search) | SharePoint knowledge base fully populated | SharePoint Search API |
| Claude Desktop (Amanda's interface) | Copilot Studio MCP integration validated | Copilot Studio agent |

---

## Appendix: How to Add Deprecation Entries

When deprecating infrastructure:

1. **Document the what:** Specific components, files, tools being removed
2. **Document the why:** Root cause analysis, not just symptoms
3. **Document the alternative:** What was considered, what was selected
4. **Document the migration:** How to move from old to new
5. **Preserve the artifacts:** Archive, don't delete — future engineers need context

---

*Document Version: 1.0*  
*Last Updated: January 31, 2026*  
*Owner: Aaron Shirley (CSO)*

