---
original_file: "OPERATIONS_MANUAL_V2_2_1"
processed_date: 2026-02-02T15:35:39.705340
type: document_extraction
---

# Document Extraction: OPERATIONS_MANUAL_V2_2_1

# Operations Manual

February 3, 2026

# OPERATIONS_MANUAL.md

Charter & Stone Automation Stack  
Version: 2.2 (Analyst V1.1 + Outreach Architect V1.0)  
Last Updated: February 3, 2026  
Platform: Raspberry Pi 5 (Heath, TX) + Microsoft 365 Cloud Services

---

## 1. SYSTEM ARCHITECTURE

```
charter-stone-automation/
â”œâ”€â”€ agents/
â”‚   â”œâ”€â”€ daemon/              # 24/7 Scheduler
â”‚   â”œâ”€â”€ watchdog/            # News Scanner
â”‚   â”œâ”€â”€ orchestrator/        # Task Router (Watchdog â†’ Strategy)
â”‚   â”œâ”€â”€ analyst/             # Deep Dive Financial Analysis [NEW V1.1]
â”‚   â”‚   â”œâ”€â”€ analyst.py       # Main orchestrator (dual output)
â”‚   â”‚   â”œâ”€â”€ sources/
â”‚   â”‚   â”‚   â”œâ”€â”€ propublica.py    # ProPublica 990 API wrapper
â”‚   â”‚   â”‚   â””â”€â”€ signals.py       # Distress signal database
â”‚   â”‚   â””â”€â”€ templates/
â”‚   â”‚       â””â”€â”€ dossier.md       # Markdown template
â”‚   â””â”€â”€ sentinel/            # Document Converter
│   └── outreach/            # Email Draft Generation [NEW V1.0]
│       ├── outreach.py      # Main orchestrator
│       ├── config/
│       │   └── system_prompt.txt    # LLM instructions
│       ├── outputs/         # Generated email sequences
│       └── logs/            # Execution logs
â”œâ”€â”€ shared/
â”‚   â”œâ”€â”€ auth.py              # Central Authentication Module
â”‚   â”œâ”€â”€ planner_client.py    # Microsoft Planner API Wrapper
â”‚   â”œâ”€â”€ config.py            # Environment Variables
â”‚   â””â”€â”€ schemas/             # Data Contracts [NEW V1.0.0]
â”‚       â””â”€â”€ prospect_profile.schema.json
â”œâ”€â”€ knowledge_base/
â”‚   â””â”€â”€ prospects/           # Analyst output directory [NEW]
â”‚       â”œâ”€â”€ [ein]_profile.json       # Machine-readable (schema v1.0.0)
â”‚       â””â”€â”€ [name]_dossier.md        # Human-readable
â”œâ”€â”€ systemd/
â”‚   â””â”€â”€ charterstone.service # Production Service Definition
â””â”€â”€ requirements.txt         # Python Dependencies
```

Purpose: Single source of truth for Microsoft Graph API authentication.

Key Features:
- Device Code Flow: Interactive browser-based login for delegated permissions
- Token Caching: Stores tokens locally (~90 day expiration)
- Auto-Refresh: Automatically renews expired tokens without re-authentication
- Required Scopes:
  - Tasks.ReadWrite - Planner task management
  - Group.Read.All - Access to team resources
  - User.Read - User profile data

Authentication Flow:
1. Agent requests token via auth.py
2. If no cached token exists, device code prompt displays
3. User visits https://microsoft.com/devicelogin and enters code
4. Token stored in ~/.cache/msal_token_cache.bin
5. All subsequent requests use cached token until expiration

Critical Note: Authentication persists across agent restarts. Re-authentication only required after ~90 days or if cache file is deleted.

---

## 2. THE STAFF (AGENTS)

### 2.1 The Daemon (Scheduler)

Location: agents/daemon/  
Purpose: Orchestrates timed execution of all other agents  
Runtime: Continuous background service via systemd

Operational Logic:
```
Schedule:
- Watchdog: Every 30 minutes
- Orchestrator: Every 60 minutes
- Sentinel: Continuous (inotify on _INBOX folder)
- Analyst: On-demand (manual invocation or triggered by orchestrator)
```

Key Functions:
- Prevents overlapping executions (process locking)
- Logs all agent invocations to systemd journal
- Handles graceful shutdown on SIGTERM

Configuration:
- Managed via /etc/systemd/system/charterstone.service
- Runs as user aaronshirley751 (non-root for security)
- Auto-restart on failure with 30s backoff

---

### 2.2 The Watchdog (News Scanner)

Location: agents/watchdog/  
Purpose: Monitors higher education news sources for institutional signals

Data Sources:
- RSS feeds from InsideHigherEd, Chronicle of Higher Education
- Web scraping of state higher ed commission announcements
- Keyword filters: "enrollment decline," "budget deficit," "restructuring"

Critical Filter:
```python
AGE_THRESHOLD = 30 days
# Prevents duplicate alerts on stale news
```

Workflow:
1. Fetch RSS feeds every 30 minutes (daemon-controlled)
2. Parse article titles/summaries for trigger keywords
3. Check article publish date (skip if >30 days old)
4. Create Planner task in "Watchdog Inbox" bucket if match found
5. Post summary to Teams webhook

Output Format (Planner Task):
```
Title: [University Name] - [Trigger Keyword]
Description: Article summary + source URL
Bucket: Watchdog Inbox
Priority: Medium (Important if contains "budget" or "layoff")
```

Known Issue: Does not deduplicate articles already seen. Use janitor.py weekly to clean duplicates.

---

### 2.3 The Orchestrator (Task Router)

Location: agents/orchestrator/  
Purpose: Routes tasks from Watchdog Inbox to Strategy bucket with basic classification

**Note:** As of V2.1, deep financial analysis has been moved to the Analyst Agent. The Orchestrator now focuses on task routing and basic classification only.

Workflow:
1. Scan "Watchdog Inbox" bucket for unprocessed tasks
2. Extract university name from task title
3. Apply basic classification logic
4. Move task to "Strategy & Intel" bucket
5. Auto-assign to Aaron Shirley (User ID: b0c032d0-5d31-48e1-8263-5cc817aa63e9)
6. Flag tasks for Analyst follow-up if financial distress keywords detected

Classification Logic:
```python
if "budget" in title.lower() or "deficit" in title.lower():
    priority = "Urgent"
    flag_for_analyst = True
elif "layoff" in title.lower() or "restructuring" in title.lower():
    priority = "Important"
    flag_for_analyst = True
else:
    priority = "Medium"
    flag_for_analyst = False
```

---

### 2.4 The Analyst (Deep Dive Financial Analysis) [NEW â€” V1.1]

Location: agents/analyst/  
Purpose: Generates comprehensive financial dossiers and structured prospect profiles from IRS 990 data  
Version: 1.1 (Dual Output Architecture)

**Data Source:** ProPublica Nonprofit Explorer API (IRS Form 990 data)

**Dual Output:**
The Analyst produces two complementary outputs for each target institution:

| Output | Format | Purpose | Filename Pattern |
|--------|--------|---------|------------------|
| Dossier | Markdown (.md) | Human-readable analysis | `[name]_dossier.md` |
| Profile | JSON (.json) | Machine-readable, schema-compliant | `[ein]_profile.json` |

**Output Location:** `~/charter_stone/knowledge_base/prospects/`

**Usage:**
```bash
cd ~/charter_stone/agents/analyst
source ../../venv/bin/activate
python3 analyst.py --target "Albright College" --ein "23-1352607"
```

**Expected Output:**
```
[ANALYST] â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
[ANALYST] Charter & Stone â€” Deep Dive Analyst Agent analyst-v1.1
[ANALYST] â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
[ANALYST] Target: Albright College
[ANALYST] EIN: 23-1352607
[ANALYST] â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
[ANALYST] Fetching ProPublica data...
[ANALYST] âœ“ Financial data retrieved (FY2023)
[ANALYST] Fetching distress signals...
[ANALYST] âœ“ 3 signal(s) retrieved
[ANALYST] Building JSON profile (schema v1.0.0)...
[ANALYST] âœ“ Profile built (distress_level: critical)
[ANALYST] â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
[ANALYST] âœ“ COMPLETE in 2.73 seconds
[ANALYST] â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ“„ Markdown Dossier: ~/charter_stone/knowledge_base/prospects/albright_college_dossier.md
ðŸ“Š JSON Profile:     ~/charter_stone/knowledge_base/prospects/231352607_profile.json
â±ï¸  Elapsed Time:     2.73s
```

**Calculated Metrics (Computed in Python):**

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| `expense_ratio` | total_expenses / total_revenue | >1.0 = deficit spending |
| `runway_years` | net_assets / annual_deficit | Years until depletion (if deficit) |
| `tuition_dependency` | tuition_revenue / total_revenue | Revenue concentration risk |

**Distress Classification Logic:**
```python
if expense_ratio > 1.2 or runway_years < 2 or critical_signals >= 2:
    distress_level = "critical"
elif expense_ratio > 1.0 or runway_years < 4 or critical_signals >= 1:
    distress_level = "elevated"
elif expense_ratio > 0.95 or warning_signals >= 2:
    distress_level = "watch"
else:
    distress_level = "stable"
```

**Blinded Presentation:**
The JSON profile includes a `blinded_presentation` block for use in external materials (pitch decks, case studies):
```json
{
  "blinded_presentation": {
    "display_name": "Representative Private Nonprofit College (Northeast)",
    "approved_for_external": false
  }
}
```

**API Rate Limits:**
- ProPublica: 100 requests/hour per IP
- Analyst processes one target at a time (sequential)

**Error Handling:**
- If 990 data not found, logs error and exits
- Network failures trigger retry with exponential backoff (max 3 attempts)
- Null values in API response handled gracefully (fields set to null in JSON)

### 2.5 The Outreach Architect (Email Draft Generation) [NEW – V1.0]

Location: agents/outreach/  
Purpose: Converts Deep Dive Analyst intelligence into actionable cold outreach email sequences  
Version: 1.0 (Production-Ready)  
Status: ✅ DEPLOYED (February 2, 2026)

**Input:** `prospect_profile.json` (schema v1.0.0) from Analyst Agent  
**Output:** 3-stage email sequence (Cold Intro → Value Add → Break-up)

**Key Features:**
- Tailors tone to institutional distress level (critical/elevated/watch)
- Enforces "Anti-Vendor" voice with hard-coded forbidden phrase filter
- Validates output against 17 banned phrases (subservient language, vendor jargon)
- Generates McKinsey-grade, peer-to-peer advisor voice
- Outputs to agents/outreach/outputs/ for manual human review

**Usage:**
```bash
cd ~/charter_stone/agents/outreach
source ../../venv/bin/activate
python3 outreach.py knowledge_base/prospects/231352607_profile.json
```

**Expected Output:**
```
============================================================
OUTREACH ARCHITECT EXECUTION SUMMARY
============================================================
STATUS: success
FILE_PATH: agents/outreach/outputs/albright_college_outreach_sequence.md
INSTITUTION: Albright College
DISTRESS_LEVEL: elevated
EMAILS_GENERATED: 3
VIOLATIONS: []
============================================================

✓ Outreach sequence generated successfully
📄 Output: agents/outreach/outputs/albright_college_outreach_sequence.md
```

**Email Sequence Structure:**

| Email | Timing | Purpose | Key Elements |
|-------|--------|---------|--------------|
| **1: Cold Intro** | Day 0 | Establish credibility | Fact-based subject, diagnostic offer, peer empathy |
| **2: Value Add** | Day 5-7 | Share intelligence | Financial data, runway calculations, crisis framing |
| **3: Break-up** | Day 10-14 | Professional close | No guilt trips, leave door open, high-status exit |

**Timing Cadence by Distress Level:**
```
Critical:  [0, 3, 7] days   (faster cadence for imminent crisis)
Elevated:  [0, 5, 10] days  (standard cadence)
Watch:     [0, 7, 14] days  (measured cadence)
Stable:    Agent aborts     (no outreach warranted)
```

**Quality Assurance:**
- **Forbidden Phrase Filter:** 17 hard-coded phrases blocked (e.g., "I wanted to share", "just checking in", "transformation", "synergy")
- **Voice Validation:** System prompt enforces imperative voice, blocks ALL "I wanted to..." constructions
- **McKinsey Partner Test:** All emails must maintain peer-level crisis advisor posture

**Anti-Vendor Positioning:**
Every email explicitly signals: "This is not a vendor call—we don't sell software. We advise on operational turnarounds."

**Human-in-the-Loop:**
- Agent NEVER sends emails automatically
- All output requires Aaron/Amanda approval before send
- Agent does NOT access email systems or store contact information

**Hotfix History:**
- **V1.0 (Feb 2, 2026):** Production deployment after QA audit
  - Expanded forbidden phrases list (added "I wanted to share", "I wanted to follow up", "I'd love to")
  - Enhanced system prompt with pattern guidance for imperative voice
  - Validated output achieves 99% compliance (upgraded from 95%)

**API Dependencies:**
- Anthropic Claude API (Sonnet 4.5) for email generation
- ProPublica 990 data (via Analyst) for financial intelligence

**Known Limitations:**
- Requires valid prospect_profile.json (schema v1.0.0)
- Aborts generation for "stable" distress level institutions
- Output quality depends on accuracy of Analyst input data

---


---

### 2.6 The Sentinel (Document Converter)

Location: agents/sentinel/ (previously root src/)  
Purpose: Converts Markdown strategy reports to branded Word documents and syncs to SharePoint

Hardware: Raspberry Pi 5 in Heath, TX (always-on physical node)

Workflow:
1. Ingestion: Monitor src/_INBOX/ folder for .md files
2. Conversion:
   - Parse Markdown to HTML
   - Apply Charter & Stone template (Reference.docx)
   - Insert title, date, and body content
   - Generate filename: Report_[Name]_[Timestamp].docx
3. Upload: Save to Rclone-mounted SharePoint directory
4. Safety Buffer: Wait 20 seconds for cloud sync to complete
5. Notification: Post Adaptive Card to Teams with direct document link
6. Cleanup: Rename .md file to .md.processed to prevent reprocessing

Critical Configuration (charterstone.service):
```ini
ExecStartPre=-/bin/fusermount -uz /home/aaronshirley751/charterstone-mount
ExecStartPre=/usr/bin/mkdir -p /home/aaronshirley751/charterstone-mount
ExecStartPre=/usr/bin/rclone mount charterstone: /home/aaronshirley751/charterstone-mount \
  --vfs-cache-mode writes \
  --no-checksum \
  --no-modtime \
  --ignore-size \
  --daemon \
  --allow-non-empty
```

"Golden Flags" Rationale:
- --vfs-cache-mode writes: Buffers writes locally until file close (prevents partial uploads)
- --no-checksum + --ignore-size: SharePoint modifies metadata post-upload, causing false corruption errors
- --no-modtime: Ignores timestamp drift between local and cloud
- fusermount -uz: Force unmount on service start to clear zombie processes

Known Limitations:
- 20-second delay is empirical; very large files (>50MB) may need longer buffer
- If SharePoint is down, files accumulate in local sync folder until connectivity restored

---

## 3. DATA CONTRACTS [NEW â€” V1.0.0]

### 3.1 Prospect Data Standard (Schema v1.0.0)

Location: shared/schemas/prospect_profile.schema.json  
Purpose: Canonical format for institution intelligence across all Digital Teammates

**Schema Sections:**

| Section | Purpose | Agents |
|---------|---------|--------|
| `meta` | Data provenance, versioning, timestamps | All (audit trail) |
| `institution` | Core identity: name, EIN, type, location | Analyst (writes), Outreach (reads) |
| `financials` | IRS 990 data + calculated metrics | Analyst (writes), Outreach (reads) |
| `signals` | Distress indicators, news hits | Watchdog (writes), Analyst (enriches) |
| `leadership` | Key contacts, stability notes | Analyst (writes), Outreach (reads) |
| `engagement` | CRM state: status, priority, owner | All (read/write) |
| `blinded_presentation` | Anonymized display for external use | Deck generation, case studies |

**Agent Communication Contract:**
```
Watchdog â†’ signals (news hits)
     â†“
Analyst â†’ profile.json (full schema)
     â†“
Outreach Architect â†’ email drafts (reads profile.json)
```

**Validation:**
All agents outputting JSON must conform to the schema. Non-conformant output will break downstream agents.

---

## 4. DEPLOYMENT (RASPBERRY PI 5)

### Hardware Specifications

- Model: Raspberry Pi 5 (8GB RAM)
- OS: Raspberry Pi OS (64-bit, Debian-based)
- Network: Ethernet (static IP: 192.168.1.100)
- Storage: 128GB microSD + 1TB external SSD (SharePoint cache)
- Location: Heath, TX (residential network)

### Initial Setup

Step 1: Clone Repository
```bash
cd /home/aaronshirley751
git clone https://github.com/charter-stone/automation.git charter-and-stone-automation
cd charter-and-stone-automation
```

Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Step 3: Configure Environment Variables
```bash
cd agents/sentinel
nano .env
```

Add the following:
```ini
TARGET_ROOT=/home/aaronshirley751/charterstone-mount/Strategy-Intel
SHAREPOINT_FOLDER_URL=https://charterandstone.sharepoint.com/sites/Operations/Shared%20Documents/Strategy-Intel
TEAMS_WEBHOOK_URL=https://prod-123.eastus.logic.azure.com:443/workflows/abc123.../triggers/manual/paths/invoke
```

Step 4: Authenticate Microsoft Graph
```bash
cd /home/aaronshirley751/charter-and-stone-automation
source venv/bin/activate
python3 -c "from shared.auth import get_graph_token; get_graph_token()"
```

Expected Output:
```
To sign in, use a web browser to open https://microsoft.com/devicelogin
and enter the code: ABCD-1234
```

1. Open browser, visit URL, enter code
2. Sign in with Aaron's Microsoft 365 account
3. Accept permissions prompt
4. Token cached to ~/.cache/msal_token_cache.bin

Verification:
```bash
ls -lh ~/.cache/msal_token_cache.bin
# Should show file ~1KB, modified within last minute
```

### Service Installation

Step 1: Copy Service File
```bash
sudo cp systemd/charterstone.service /etc/systemd/system/
sudo nano /etc/systemd/system/charterstone.service
```

Verify Paths Match Your Setup:
```ini
[Service]
User=aaronshirley751
WorkingDirectory=/home/aaronshirley751/charter-and-stone-automation
ExecStart=/home/aaronshirley751/charter-and-stone-automation/venv/bin/python \
  /home/aaronshirley751/charter-and-stone-automation/agents/daemon/scheduler.py
```

Step 2: Configure Rclone Remote
```bash
rclone config
# Name: charterstone
# Type: Microsoft SharePoint
# Client ID: (use default)
# Client Secret: (leave blank for device auth)
# Follow OAuth prompts
```

Step 3: Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable charterstone.service
sudo systemctl start charterstone.service
```

Step 4: Verify Operation
```bash
sudo systemctl status charterstone.service
# Expected: "active (running)" in green
```

### Verification Checklist

- [ ] Service status shows active (running)
- [ ] Rclone mount exists: `ls /home/aaronshirley751/charterstone-mount`
- [ ] Drop test .md file into agents/sentinel/src/_INBOX/
- [ ] Verify .docx appears in SharePoint within 60 seconds
- [ ] Teams channel receives notification with clickable link
- [ ] Original .md file renamed to .md.processed
- [ ] Run Analyst test: `python3 agents/analyst/analyst.py --target "Test College" --ein "12-3456789"`
- [ ] Verify JSON + Markdown output in knowledge_base/prospects/

---

## 5. MAINTENANCE

### Logging

Real-Time Monitoring:
```bash
# Follow logs as they happen
sudo journalctl -u charterstone -f

# Last 100 lines
sudo journalctl -u charterstone -n 100

# Last 24 hours
sudo journalctl -u charterstone --since "24 hours ago"

# Filter by keyword
sudo journalctl -u charterstone | grep ERROR
```

Log Interpretation:

| Pattern | Meaning | Action Required |
|---------|---------|-----------------|
| ðŸ“£ Teams Alert Sent (202 Accepted) | Normal operation | None |
| âš ï¸ Skipping Teams Alert (Webhook URL not set) | Missing .env variable | Check TEAMS_WEBHOOK_URL in .env |
| âŒ Error: [Errno 2] No such file | Template missing | Verify Reference.docx exists |
| fusermount: entry for ... not found | Clean state (normal on first start) | None |
| 429 Too Many Requests | API rate limit hit | Wait 60 minutes, then retry |
| [ANALYST] âœ“ COMPLETE | Analyst finished successfully | None |
| [ANALYST] [ERROR] No financial data found | EIN not in ProPublica | Verify EIN format |

Automatic Cleanup:
- Systemd journal automatically rotates logs when size exceeds 5MB
- Old logs compressed and archived to /var/log/journal/
- Retention: 7 days of active logs, 30 days of compressed archives

Manual Rotation (if needed):
```bash
# Force rotation now
sudo journalctl --rotate

# Vacuum logs older than 7 days
sudo journalctl --vacuum-time=7d

# Limit total journal size to 500MB
sudo journalctl --vacuum-size=500M
```

Disk Space Monitoring:
```bash
# Check journal disk usage
journalctl --disk-usage

# Check mount point usage
df -h /home/aaronshirley751/charterstone-mount

# Check knowledge_base size
du -sh ~/charter_stone/knowledge_base/
```

### Duplicate Task Cleanup

Problem: Watchdog may create duplicate tasks if an article is re-indexed by RSS feeds.

Solution: Run janitor.py weekly to detect and archive duplicates.

Usage:
```bash
cd /home/aaronshirley751/charter-and-stone-automation
source venv/bin/activate
python3 shared/janitor.py
```

What It Does:
1. Scans all tasks in "Watchdog Inbox" bucket
2. Identifies tasks with identical titles
3. Keeps the oldest task (earliest creation date)
4. Moves duplicates to "Archive" bucket
5. Logs actions to console

Output Example:
```
Found 3 duplicate tasks for "University of Texas - Enrollment Decline"
Keeping task #1 (created 2026-01-15)
Archiving task #2 (created 2026-01-20)
Archiving task #3 (created 2026-01-22)
Total duplicates archived: 2
```

Scheduling (Optional):
```bash
# Add to crontab for automatic weekly runs
crontab -e

# Add line:
0 2 * * 0 /home/aaronshirley751/charter-and-stone-automation/venv/bin/python3 /home/aaronshirley751/charter-and-stone-automation/shared/janitor.py >> /tmp/janitor.log 2>&1
# Runs every Sunday at 2:00 AM
```

### Service Management

Graceful Restart (Recommended):
```bash
sudo systemctl restart charterstone.service
```

Hard Stop/Start (If Unresponsive):
```bash
sudo systemctl stop charterstone.service
# Wait 10 seconds
sudo systemctl start charterstone.service
```

After Configuration Changes:
```bash
# If .env or Python code changed
sudo systemctl restart charterstone.service

# If .service file changed
sudo systemctl daemon-reload
sudo systemctl restart charterstone.service
```

### Common Issues

**Issue: Service won't start - "Failed to mount"**

Cause: Stale Rclone process or corrupted mount  
Fix:
```bash
sudo fusermount -uz /home/aaronshirley751/charterstone-mount
sudo systemctl restart charterstone.service
```

**Issue: Teams notifications not arriving**

Cause: Webhook URL expired or malformed  
Fix:
1. Regenerate webhook in Power Automate
2. Update TEAMS_WEBHOOK_URL in .env
3. Restart service

**Issue: SharePoint sync delayed (>5 minutes)**

Cause: Network congestion or Rclone cache backlog  
Fix:
```bash
# Check mount health
ls -lh /home/aaronshirley751/charterstone-mount

# Force sync flush
rclone rc vfs/forget file=/home/aaronshirley751/charterstone-mount/*

# If persists, remount
sudo systemctl restart charterstone.service
```

**Issue: Authentication expired (after 90 days)**

Symptoms: Logs show 401 Unauthorized or AADSTS50078  
Fix:
```bash
# Delete cached token
rm ~/.cache/msal_token_cache.bin

# Re-authenticate
python3 -c "from shared.auth import get_graph_token; get_graph_token()"

# Follow device code flow prompts
```

**Issue: Analyst returns no data**

Symptoms: "No financial data found" error  
Fix:
1. Verify EIN format is XX-XXXXXXX (with dash)
2. Check ProPublica manually: https://projects.propublica.org/nonprofits/
3. Some small institutions may not have 990 filings

### Health Check

Location: shared/healthcheck.sh

Run Weekly:
```bash
cd /home/aaronshirley751/charter-and-stone-automation
bash shared/healthcheck.sh
```

Checks Performed:
- [ ] Service status (running/failed)
- [ ] Rclone mount accessibility
- [ ] Recent log errors (last 1 hour)
- [ ] Disk space on mount (warn if >80% full)
- [ ] Token expiration (warn if <7 days remaining)
- [ ] Last successful Teams notification (warn if >24 hours)
- [ ] Knowledge base directory exists and writable

Output:
```
[âœ“] charterstone.service is active
[âœ“] Rclone mount is accessible
[!] Warning: 2 ERROR entries in last hour
[âœ“] Disk usage: 45% (safe)
[âœ“] Token expires in 62 days
[âœ“] Last Teams alert: 2 hours ago
[âœ“] Knowledge base writable
```

---

## 6. OPERATIONAL NOTES

### Power & Network

Pi 5 Power Loss Handling:
- Service configured with Restart=always in systemd
- On unexpected shutdown, service auto-restarts on boot
- Rclone mount state does NOT persist across reboots
- First boot after power loss takes ~60 seconds (mount initialization)

Planned Shutdowns:
```bash
# Graceful shutdown (recommended)
sudo systemctl stop charterstone.service
sudo shutdown -h now

# Fast shutdown (emergency only)
sudo poweroff
```

Bandwidth:
- Upload: ~10 Mbps (for large document syncs)
- Download: ~5 Mbps (for RSS feeds, 990 PDFs)

Firewall Ports:
- Outbound 443 (HTTPS): Required for all API calls
- Outbound 53 (DNS): Required for domain resolution

Static IP Recommended:
- Prevents DHCP lease conflicts on router reboots
- Set in /etc/dhcpcd.conf on Pi

### Backup Strategy

Critical Files to Backup (Daily):
- ~/.cache/msal_token_cache.bin (authentication)
- agents/sentinel/.env (configuration)
- /etc/systemd/system/charterstone.service (service definition)
- ~/charter_stone/knowledge_base/ (analyst outputs) [NEW]
- shared/schemas/ (data contracts) [NEW]

Automated Backup (via Rclone):
```bash
# Add to crontab
0 3 * * * rclone sync ~/.cache/msal_token_cache.bin charterstone:Backups/tokens/
0 3 * * * rclone sync ~/charter_stone/knowledge_base/ charterstone:Backups/knowledge_base/
```

### Alerting

Current Setup:
- Teams notifications for document processing
- Analyst completion notifications (via console output)

Future Enhancements (Roadmap):
- ~~Mirror Agent: RAG-based document Q&A demo~~ [CANCELLED â€” conflicts with Anti-SaaS positioning]
- Dead Man's Switch: Alert if no activity for 6 hours
- Disk space alerts when mount >80% full
- Token expiration warnings at 7 days remaining
- Outreach Architect: Email draft generation from prospect profiles [âœ… DEPLOYED - V1.0, Feb 2, 2026]
- The Mechanic: Infrastructure health monitoring agent [PLANNED]

---

## 7. DIGITAL TEAMMATES ROSTER [NEW]

| Agent | Status | Purpose | Output |
|-------|--------|---------|--------|
| **Daemon** | âœ… LIVE | Scheduler, process orchestration | Logs |
| **Watchdog** | âœ… LIVE | News monitoring, signal detection | Planner tasks |
| **Orchestrator** | âœ… LIVE | Task routing, basic classification | Planner updates |
| **Analyst** | âœ… LIVE (V1.1) | Financial analysis, dossier generation | JSON + Markdown |
| **Sentinel** | âœ… LIVE | Document conversion, SharePoint sync | .docx files |
| **Outreach Architect** | âœ… LIVE (V1.0) | Email draft generation | Email drafts |
| **The Mechanic** | ðŸ“‹ PLANNED | Infrastructure health monitoring | Alerts, Planner tasks |
| ~~**Mirror**~~ | âŒ CANCELLED | ~~RAG document Q&A~~ | â€” |

---

## 8. CONTACT & ESCALATION

System Administrator: Aaron Shirley  
Escalation Path:
1. Check logs: `journalctl -u charterstone -n 100`
2. Attempt service restart: `sudo systemctl restart charterstone.service`
3. If authentication errors: Re-run device code flow
4. If persistent failures: Post in Teams "#Tech-Support" channel

Microsoft Support Contacts:
- Graph API issues: https://aka.ms/graphsupport
- SharePoint sync issues: Submit ticket via M365 Admin Center

---

## DOCUMENT HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-15 | Initial release |
| 2.0 | 2026-01-29 | Digital Teammates Architecture |
| **2.1** | **2026-02-03** | Added Analyst V1.1 (dual output), Prospect Data Schema v1.0.0, updated agent roster, cancelled Mirror Agent |
| **2.2** | **2026-02-03** | Added Outreach Architect V1.0 (production-ready email generation), expanded agent roster with deployment status, updated architecture diagram |

---

END OF OPERATIONS MANUAL

