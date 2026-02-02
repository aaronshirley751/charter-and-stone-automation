# Charter & Stone Automation Server (Sentinel)

**Status:** ✅ Active Duty (Operation Sentinel + Analyst V1.1)  
**System:** Raspberry Pi 5 (Headless / Silent Mode)  
**Latest Deployment:** Analyst Agent V1.1 (2 Feb 2026)

An intelligent automation system featuring:
- **Sentinel Agent:** Automated document processing and SharePoint publishing
- **Analyst Agent V1.1:** Financial intelligence and prospect profiling (NEW)
- **Watchdog Agent:** News monitoring and distress signal detection (planned)

## System Overview

### Sentinel Agent (Document Pipeline)
Monitors local folder for Markdown files, converts them into branded Word documents, and publishes notifications to Microsoft Teams via Power Automate Webhooks.

**Features:**
- **Automated Conversion:** Watches `src/_INBOX` for new `.md` files.
- **Branding:** Applies Charter & Stone styles using reference Word template.
- **Reliable Cloud Sync:** Uses hardened `rclone` mount settings for SharePoint.
- **Notifications:** Sends rich Adaptive Cards to Microsoft Teams.
- **Self-Healing:** "Breach and Clear" protocols handle stale mounts.

### Analyst Agent V1.1 (NEW - Financial Intelligence)
Generates comprehensive financial dossiers for higher education institutions using IRS 990 data.

**Features:**
- **Dual Output:** Markdown dossier (human-readable) + JSON profile (machine-readable)
- **Schema Compliance:** Outputs conform to Prospect Data Standard v1.0.0
- **Calculated Metrics:** Expense ratio, runway years, tuition dependency
- **Distress Classification:** Automatic risk assessment (critical/elevated/watch/stable)
- **Null-Safe:** Robust handling of missing financial data
- **ProPublica Integration:** Fetches IRS 990 data from public API

**Usage:**
```bash
python3 agents/analyst/analyst.py --target "University Name" --ein "XX-XXXXXXX"
```

**Output:**
- `~/charter_stone/knowledge_base/prospects/{EIN}_profile.json` - Machine-readable
- `~/charter_stone/knowledge_base/prospects/{name}_dossier.md` - Human-readable

**Documentation:**
- [Analyst V1.1 Peer Review](ANALYST_V1.1_PEER_REVIEW.md)
- [Sources Module Integration Review](SOURCES_MODULE_INTEGRATION_REVIEW.md)
- [Deployment Log V1.1](DEPLOYMENT_LOG_V1.1.md)

## Setup & Configuration

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd charter-and-stone-automation
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the project root directory:

    ```ini
    TARGET_ROOT=/home/aaronshirley751/charterstone-mount/Operations
    SHAREPOINT_FOLDER_URL=https://charterandstone.sharepoint.com/sites/CharterStone/Shared%20Documents/Operations
    TEAMS_WEBHOOK_URL=https://your-power-automate-webhook-url
    TEMPLATE_PATH=/home/aaronshirley751/charter-and-stone-automation/agents/sentinel/templates/charter_template.docx
    ```

4.  **Systemd Service (The "Golden Config"):**
    The `charterstone.service` file is critical for stability. It includes specific flags to handle SharePoint's metadata behavior:
    - `--vfs-cache-mode writes`: Delays upload until file close.
    - `--ignore-checksum` & `--no-checksum`: Prevents false "corruption" errors from SharePoint metadata modification.
    - `--ignore-size`: Ignores file size changes post-upload.
    - `--no-modtime`: Ignores timestamp drifts.

## Current Architecture

**Unified Site:** All operations now route through the unified "CharterStone" SharePoint site.

**Active Components:**
- **Sentinel Agent:** Raspberry Pi 5 running Ubuntu at Heath, TX
- **Analyst Agent V1.1:** Financial intelligence system (Python 3.11+)
- **rclone Mount:** FUSE filesystem at `/home/aaronshirley751/charterstone-mount`
- **Systemd Service:** `charterstone.service` (active, PID 67672)
- **Document Pipeline:** Markdown → Branded DOCX → SharePoint Operations folder
- **SharePoint Structure:** 7 folders (General, Governance, Incoming Signals, Intelligence, Operations, Strategy and Intel, Technical)
- **Knowledge Base:** Prospect profiles stored in `~/charter_stone/knowledge_base/prospects/`

**File Paths:**
- Sentinel Inbox: `agents/sentinel/_INBOX/`
- Sentinel Output: `agents/sentinel/_OUTPUT/`
- Sentinel Templates: `agents/sentinel/templates/charter_template.docx`
- Analyst Agent: `agents/analyst/analyst.py`
- Analyst Sources: `agents/analyst/sources/` (propublica.py, signals.py)
- Prospect Profiles: `~/charter_stone/knowledge_base/prospects/`
- SharePoint Mount: `/home/aaronshirley751/charterstone-mount/`

---

## Usage

The system runs as a background service (`charterstone.service`).

To manually trigger or test:
```bash
cd /home/aaronshirley751/charter-and-stone-automation/agents/sentinel
python converter.py
```

Drop a Markdown file into `agents/sentinel/_INBOX`. The system will:
1.  Detect the file.
2.  Convert to `.docx` with branding from `charter_template.docx`.
3.  Upload to SharePoint Operations folder.
4.  Move processed file to `_OUTPUT` with timestamp.

## Service Management

Check service status:
```bash
sudo systemctl status charterstone.service
```

Restart service:
```bash
sudo systemctl restart charterstone.service
```

View logs:
```bash
sudo journalctl -u charterstone.service -f
```

Check mount status:
```bash
ls -la /home/aaronshirley751/charterstone-mount/
rclone lsd charterstone:
```

## Commissioning Log

### Jan 31, 2026 — HQ Site Migration & Deprecation Verification

**Operation: Unified Site Migration**

Migrated Charter & Stone Sentinel from deprecated "Charter & Stone HQ" SharePoint site to unified "CharterStone" site. Performed comprehensive verification to ensure no operational remnants remain.

**Key Changes:**
- ✅ **Environment Configuration:** Updated `.env` with unified site paths
  - `TARGET_ROOT=/home/aaronshirley751/charterstone-mount/Operations`
  - `SHAREPOINT_FOLDER_URL=https://charterandstone.sharepoint.com/sites/CharterStone/Shared%20Documents/Operations`
- ✅ **Systemd Service Fix:** Corrected `charterstone.service` paths
  - WorkingDirectory: `/home/aaronshirley751/charter-and-stone-automation/agents/sentinel`
  - ExecStart: Changed from `auto_publisher.py` (non-existent) to `converter.py`
- ✅ **Template Setup:** Created `charter_template.docx` in `agents/sentinel/templates/`
- ✅ **rclone Configuration:** Verified drive_id points to unified site (b!xv2k...JjKb)
- ✅ **Live Testing:** Successfully converted test documents with branding applied
- ✅ **Ghost Hunt:** Comprehensive verification found zero active references to deprecated site

**Verification Results:**
- Rclone configuration: CLEAN ✅
- Python code references: CLEAN ✅
- Systemd services: CLEAN ✅
- Live remote access: OPERATIONAL ✅
- Documentation archives: Historical references preserved for audit trail

**Documentation:**
- Generated `HQ_SITE_DEPRECATION_VERIFICATION.md` with full verification report
- Service confirmed running (PID 67672) with all 7 unified site folders accessible
- Mount point: `/home/aaronshirley751/charterstone-mount`

---

### Jan 26, 2026 — Operation Sentinel

**Operation Sentinel** stabilized the pipeline with the following resolutions:

-   **Zombie Lock Fix:** Added `fusermount -uz` pre-start command to clear stale mounts.
-   **Ghost Drive Fix:** Enforced strict dependency ordering in systemd.
-   **Race Condition Fix:** Added tactical delay to `auto_publisher.py` to ensure upload completion before notification.
-   **SharePoint Compatibility:** Applied "Golden Flags" to `rclone` to ignore cloud-side metadata changes that caused file deletion/corruption errors.
