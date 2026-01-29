# CHARTER & STONE AI BEHAVIORAL PROTOCOLS

## 1. THE PRIME DIRECTIVE: READ THE MANUAL
Before generating code or answering architectural questions, you MUST ingest the context from `OPERATIONS_MANUAL.md`. This file is the Source of Truth for:
- Folder Structure (`agents/` vs `shared/`)
- Authentication (`shared.auth`)
- Deployment Paths (`/home/aaronshirley751/...`)

## 2. DOCUMENTATION AS CODE
If you propose a code change that alters the system architecture (e.g., adding a new agent, changing a schedule, modifying auth), you MUST include a corresponding update to `OPERATIONS_MANUAL.md` in the same response.
- NEVER suggest a change that makes the manual obsolete without updating the manual.

## 3. THE SENTINEL PROTOCOL
The `OPERATIONS_MANUAL.md` is the source. The SharePoint .docx is the output.
- To update the "Human Readable" version: Suggest running `cp OPERATIONS_MANUAL.md agents/sentinel/src/_INBOX/` after edits are committed.

## 4. CODING STANDARDS
- **Imports:** ALWAYS use absolute imports referencing the project root (fix `sys.path` if needed).
- **Auth:** NEVER hardcode credentials. ALWAYS import `GraphAuthenticator` from `shared.auth`.
- **Logs:** ALWAYS use `RotatingFileHandler` for long-running daemons.
