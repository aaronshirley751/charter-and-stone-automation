# ADR-022: Service-to-Service vs. Session-Based Tool Access

**Date:** 2026-02-26
**Status:** Accepted
**Author:** @systems-architect
**Deciders:** Charter & Stone Engineering

---

## Context

Watchdog is the first autonomous agent in the Charter & Stone system that
writes to shared business systems (HubSpot CRM) without any human in the loop.
It runs 24/7 as a systemd service on Pi5 — never inside an interactive Claude
session.

A parallel authentication pattern already exists for session-driven workflows
(e.g., Cornerstone, Forge): those agents access HubSpot via the **Claude MCP
HubSpot integration**, which authenticates via OAuth within an active Claude
session.

This creates two distinct access patterns for the same HubSpot instance. This
ADR defines the boundary between them and codifies it as an organisational
convention.

---

## Decision

Adopt a **dual authentication pattern** based on whether the agent runs inside
a Claude session:

| Agent Type | Runs in Claude Session? | Auth Pattern |
|---|---|---|
| Autonomous background agents (Watchdog, future Analyst background jobs) | No | HubSpot Private App token via REST API |
| Session-driven agents (Cornerstone, Forge, interactive workflows) | Yes | HubSpot MCP via OAuth |

**Canonical rule:**
> _If the agent runs inside a Claude session → use MCP. If not → use the
> Private App token via REST API._

---

## Implementation

### Autonomous agents (this ADR's primary scope)

- Authenticate with a HubSpot **Private App** token
  (`pat-na2-XXXXXXXXXXXX`).
- Token stored in `/opt/watchdog/config/watchdog.env` as
  `HUBSPOT_ACCESS_TOKEN`.
- HTTP calls made directly via `httpx` to `https://api.hubapi.com`.
- No Claude process, no MCP server, no user session required.
- First implementation: `watchdog/hubspot.py` on Pi5 at `/opt/watchdog/` (CHA-105).

### Session-driven agents

- HubSpot MCP server handles all auth transparently within the Claude session.
- No token management required in agent code.
- Operators interact via natural language; MCP translates to API calls.

---

## Rationale

1. **MCP requires a live Claude session.** It is not designed for daemon
   processes. Attempting to use MCP from a background service would require
   keeping a Claude session open indefinitely — architecturally incorrect and
   operationally fragile.

2. **Private App tokens are designed for service-to-service integration.**
   They are scoped, auditable, and revokable independently of any user account.

3. **Both patterns write to the same HubSpot instance.** There is no data
   isolation concern — Watchdog creates deals that human operators and
   session-driven agents can see and act on immediately.

4. **Clear operational boundary.** The rule is unambiguous. New agents can
   self-classify without case-by-case architectural review.

---

## Consequences

- Every future autonomous background agent (cron, APScheduler, daemon) follows
  the Private App token pattern. This is the default for non-interactive code.
- Every session-driven agent uses MCP. This is the default for interactive
  Claude workflows.
- Private App tokens must be rotated and scoped per service, not shared across
  agents. Each autonomous agent gets its own Private App.
- Token storage and rotation procedures are owned by the operator. Tokens are
  never committed to the repository.

---

## Related

- CHA-95: Watchdog Infrastructure Blueprint
- CHA-104: Watchdog Phase 2 — Perplexity Scanner
- CHA-105: Watchdog Phase 3 — HubSpot Integration
- ADR-021: Claude Code Reversion (2026-02-26)

---

*ADR number: ADR-022 (ADR-021 is Claude Code Reversion, dated 2026-02-26).*
