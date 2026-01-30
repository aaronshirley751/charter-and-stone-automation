# OPERATIONS_MANUAL.md

**Charter & Stone Automation Stack**  
**Version:** 2.0 (Digital Teammates Architecture)  
**Last Updated:** January 29, 2026  
**Platform:** Raspberry Pi 5 (Heath, TX) + Microsoft 365 Cloud Services

---

## 1. SYSTEM ARCHITECTURE

### 1.1 Monorepo Structure

```
charter-stone-automation/
├── agents/
│   ├── daemon/           # 24/7 Scheduler
│   ├── watchdog/         # News Scanner
│   ├── orchestrator/     # 990 Analysis & Router
│   └── sentinel/         # Document Converter
├── shared/
│   ├── auth.py           # Central Authentication Module
│   ├── planner_client.py # Microsoft Planner API Wrapper
│   └── config.py         # Environment Variables
├── systemd/
│   └── charterstone.service  # Production Service Definition
└── requirements.txt      # Python Dependencies
```

### 1.2 Central Authentication (`shared/auth.py`)

**Purpose:** Single source of truth for Microsoft Graph API authentication.

**Key Features:**
- **Device Code Flow:** Interactive browser-based login for delegated permissions
- **Token Caching:** Stores tokens locally (~90 day expiration)
- **Auto-Refresh:** Automatically renews expired tokens without re-authentication
- **Required Scopes:**
  - `Tasks.ReadWrite` - Planner task management
  - `Group.Read.All` - Access to team resources
  - `User.Read` - User profile data

**Authentication Flow:**
1. Agent requests token via `auth.py`
2. If no cached token exists, device code prompt displays
3. User visits `https://microsoft.com/devicelogin` and enters code
4. Token stored in `~/.cache/msal_token_cache.bin`
5. All subsequent requests use cached token until expiration

**Critical Note:** Authentication persists across agent restarts. Re-authentication only required after ~90 days or if cache file is deleted.

---

## 2. THE STAFF (AGENTS)

### 2.1 DAEMON (24/7 Scheduler)

**Location:** `agents/daemon/`  
**Purpose:** Orchestrates timed execution of all other agents  
**Runtime:** Continuous background service via `systemd`

**Operational Logic:**
```python
Schedule:
- Watchdog: Every 30 minutes
- Orchestrator: Every 60 minutes
- Sentinel: Continuous (inotify on _INBOX folder)
```

**Key Functions:**
- Prevents overlapping executions (process locking)
- Logs all agent invocations to systemd journal
- Handles graceful shutdown on SIGTERM

**Configuration:**
- Managed via `/etc/systemd/system/charterstone.service`
- Runs as user `aaronshirley751` (non-root for security)
- Auto-restart on failure with 30s backoff

---

### 2.2 WATCHDOG (News Scanner)

**Location:** `agents/watchdog/`  
**Purpose:** Monitors higher education news sources for institutional signals

**Data Sources:**
- RSS feeds from InsideHigherEd, Chronicle of Higher Education
- Web scraping of state higher ed commission announcements
- Keyword filters: "enrollment decline," "budget deficit," "restructuring"

**Critical Filter:**
```python
AGE_THRESHOLD = 30 days
# Prevents duplicate alerts on stale news
```

**Workflow:**
1. Fetch RSS feeds every 30 minutes (daemon-controlled)
2. Parse article titles/summaries for trigger keywords
3. Check article publish date (skip if >30 days old)
4. Create Planner task in "Watchdog Inbox" bucket if match found
5. Post summary to Teams webhook

**Output Format (Planner Task):**
```
Title: [University Name] - [Trigger Keyword]
Description: Article summary + source URL
Bucket: Watchdog Inbox
Priority: Medium (Important if contains "budget" or "layoff")
```

**Known Issue:** Does not deduplicate articles already seen. Use `janitor.py` weekly to clean duplicates.

---

### 2.3 ORCHESTRATOR (990 Analysis & Auto-Assignment)

**Location:** `agents/orchestrator/`  
**Purpose:** Enriches university prospect tasks with financial intelligence and routes to Strategy bucket

**Data Source:** ProPublica Nonprofit Explorer API (IRS Form 990 data)

**Workflow:**
1. Scan "Watchdog Inbox" bucket for unprocessed tasks
2. Extract university name from task title
3. Query ProPublica API for latest 990 filing
4. Extract key metrics:
   - Total revenue
   - Net assets
   - Fiscal year
   - PDF link to full 990
5. Update task description with financial snapshot
6. **Move task to "Strategy & Intel" bucket**
7. Auto-assign to Aaron Shirley (User ID: `b0c032d0-5d31-48e1-8263-5cc817aa63e9`)
8. Post enriched summary to Teams

**Classification Logic:**
```python
if revenue > $100M and net_assets > $50M:
    tier = "Tier 2 Prospect (Strong Financials)"
elif revenue_decline > 10%:
    tier = "Restructuring Giant (Operational Risk)"
else:
    tier = "Tier 3 (Monitor)"
```

**API Rate Limits:**
- ProPublica: 100 requests/hour per IP
- Orchestrator throttles to 1 query per task (sequential processing)

**Error Handling:**
- If 990 data not found, logs warning and moves task without financial data
- Network failures trigger retry with exponential backoff (max 3 attempts)

---

### 2.4 SENTINEL (Document Converter)

**Location:** `agents/sentinel/` (previously root `src/`)  
**Purpose:** Converts Markdown strategy reports to branded Word documents and syncs to SharePoint

**Hardware:** Raspberry Pi 5 in Heath, TX (always-on physical node)

**Workflow:**
1. **Ingestion:** Monitor `src/_INBOX/` folder for `.md` files
2. **Conversion:** 
   - Parse Markdown to HTML
   - Apply Charter & Stone template (`Reference.docx`)
   - Insert title, date, and body content
   - Generate filename: `Report_[Name]_[Timestamp].docx`
3. **Upload:** Save to Rclone-mounted SharePoint directory
4. **Safety Buffer:** Wait 20 seconds for cloud sync to complete
5. **Notification:** Post Adaptive Card to Teams with direct document link
6. **Cleanup:** Rename `.md` file to `.md.processed` to prevent reprocessing

**Critical Configuration (`charterstone.service`):**

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

**"Golden Flags" Rationale:**
- `--vfs-cache-mode writes`: Buffers writes locally until file close (prevents partial uploads)
- `--no-checksum` + `--ignore-size`: SharePoint modifies metadata post-upload, causing false corruption errors
- `--no-modtime`: Ignores timestamp drift between local and cloud
- `fusermount -uz`: Force unmount on service start to clear zombie processes

**Known Limitations:**
- 20-second delay is empirical; very large files (>50MB) may need longer buffer
- If SharePoint is down, files accumulate in local sync folder until connectivity restored

---

## 3. DEPLOYMENT (RASPBERRY PI 5)

### 3.1 Hardware Specifications

- **Model:** Raspberry Pi 5 (8GB RAM)
- **OS:** Raspberry Pi OS (64-bit, Debian-based)
- **Network:** Ethernet (static IP: 192.168.1.100)
- **Storage:** 128GB microSD + 1TB external SSD (SharePoint cache)
- **Location:** Heath, TX (residential network)

### 3.2 Initial Setup

**Step 1: Clone Repository**
```bash
cd /home/aaronshirley751
git clone https://github.com/charter-stone/automation.git charter-and-stone-automation
cd charter-and-stone-automation
```

**Step 2: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 3: Configure Environment Variables**
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

**Step 4: Authenticate Microsoft Graph**
```bash
cd /home/aaronshirley751/charter-and-stone-automation
source venv/bin/activate
python3 -c "from shared.auth import get_graph_token; get_graph_token()"
```

**Expected Output:**
```
To sign in, use a web browser to open https://microsoft.com/devicelogin
and enter the code: ABCD-1234
```

1. Open browser, visit URL, enter code
2. Sign in with Aaron's Microsoft 365 account
3. Accept permissions prompt
4. Token cached to `~/.cache/msal_token_cache.bin`

**Verification:**
```bash
ls -lh ~/.cache/msal_token_cache.bin
# Should show file ~1KB, modified within last minute
```

---

### 3.3 Systemd Service Installation

**Step 1: Copy Service File**
```bash
sudo cp systemd/charterstone.service /etc/systemd/system/
sudo nano /etc/systemd/system/charterstone.service
```

**Verify Paths Match Your Setup:**
```ini
[Service]
User=aaronshirley751
WorkingDirectory=/home/aaronshirley751/charter-and-stone-automation
ExecStart=/home/aaronshirley751/charter-and-stone-automation/venv/bin/python \
    /home/aaronshirley751/charter-and-stone-automation/agents/daemon/scheduler.py
```

**Step 2: Configure Rclone Remote**
```bash
rclone config
# Name: charterstone
# Type: Microsoft SharePoint
# Client ID: (use default)
# Client Secret: (leave blank for device auth)
# Follow OAuth prompts
```

**Step 3: Enable and Start Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable charterstone.service
sudo systemctl start charterstone.service
```

**Step 4: Verify Operation**
```bash
sudo systemctl status charterstone.service
# Expected: "active (running)" in green
```

---

### 3.4 First Run Checklist

- [ ] Service status shows `active (running)`
- [ ] Rclone mount exists: `ls /home/aaronshirley751/charterstone-mount`
- [ ] Logs show no authentication errors: `journalctl -u charterstone -n 50`
- [ ] Drop test `.md` file into `agents/sentinel/src/_INBOX/`
- [ ] Verify `.docx` appears in SharePoint within 60 seconds
- [ ] Teams channel receives notification with clickable link
- [ ] Original `.md` file renamed to `.md.processed`

---

## 4. MAINTENANCE

### 4.1 Viewing Logs

**Real-Time Monitoring:**
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

**Log Interpretation:**

| Pattern | Meaning | Action Required |
|---------|---------|-----------------|
| `📣 Teams Alert Sent (202 Accepted)` | Normal operation | None |
| `⚠️ Skipping Teams Alert (Webhook URL not set)` | Missing `.env` variable | Check `TEAMS_WEBHOOK_URL` in `.env` |
| `❌ Error: [Errno 2] No such file` | Template missing | Verify `Reference.docx` exists |
| `fusermount: entry for ... not found` | Clean state (normal on first start) | None |
| `429 Too Many Requests` | API rate limit hit | Wait 60 minutes, then retry |

---

### 4.2 Log Rotation

**Automatic Cleanup:**
- Systemd journal automatically rotates logs when size exceeds **5MB**
- Old logs compressed and archived to `/var/log/journal/`
- Retention: 7 days of active logs, 30 days of compressed archives

**Manual Rotation (if needed):**
```bash
# Force rotation now
sudo journalctl --rotate

# Vacuum logs older than 7 days
sudo journalctl --vacuum-time=7d

# Limit total journal size to 500MB
sudo journalctl --vacuum-size=500M
```

**Disk Space Monitoring:**
```bash
# Check journal disk usage
journalctl --disk-usage

# Check mount point usage
df -h /home/aaronshirley751/charterstone-mount
```

---

### 4.3 Planner Duplicate Cleanup (`janitor.py`)

**Problem:** Watchdog may create duplicate tasks if an article is re-indexed by RSS feeds.

**Solution:** Run `janitor.py` weekly to detect and archive duplicates.

**Usage:**
```bash
cd /home/aaronshirley751/charter-and-stone-automation
source venv/bin/activate
python3 shared/janitor.py
```

**What It Does:**
1. Scans all tasks in "Watchdog Inbox" bucket
2. Identifies tasks with identical titles
3. Keeps the oldest task (earliest creation date)
4. Moves duplicates to "Archive" bucket
5. Logs actions to console

**Output Example:**
```
Found 3 duplicate tasks for "University of Texas - Enrollment Decline"
Keeping task #1 (created 2026-01-15)
Archiving task #2 (created 2026-01-20)
Archiving task #3 (created 2026-01-22)
Total duplicates archived: 2
```

**Scheduling (Optional):**
```bash
# Add to crontab for automatic weekly runs
crontab -e

# Add line:
0 2 * * 0 /home/aaronshirley751/charter-and-stone-automation/venv/bin/python3 /home/aaronshirley751/charter-and-stone-automation/shared/janitor.py >> /tmp/janitor.log 2>&1
# Runs every Sunday at 2:00 AM
```

---

### 4.4 Restarting Services

**Graceful Restart (Recommended):**
```bash
sudo systemctl restart charterstone.service
```

**Hard Stop/Start (If Unresponsive):**
```bash
sudo systemctl stop charterstone.service
# Wait 10 seconds
sudo systemctl start charterstone.service
```

**After Configuration Changes:**
```bash
# If .env or Python code changed
sudo systemctl restart charterstone.service

# If .service file changed
sudo systemctl daemon-reload
sudo systemctl restart charterstone.service
```

---

### 4.5 Troubleshooting Common Issues

**Issue:** Service won't start - "Failed to mount"

**Cause:** Stale Rclone process or corrupted mount  
**Fix:**
```bash
sudo fusermount -uz /home/aaronshirley751/charterstone-mount
sudo systemctl restart charterstone.service
```

---

**Issue:** Teams notifications not arriving

**Cause:** Webhook URL expired or malformed  
**Fix:**
1. Regenerate webhook in Power Automate
2. Update `TEAMS_WEBHOOK_URL` in `.env`
3. Restart service

---

**Issue:** SharePoint sync delayed (>5 minutes)

**Cause:** Network congestion or Rclone cache backlog  
**Fix:**
```bash
# Check mount health
ls -lh /home/aaronshirley751/charterstone-mount

# Force sync flush
rclone rc vfs/forget file=/home/aaronshirley751/charterstone-mount/*

# If persists, remount
sudo systemctl restart charterstone.service
```

---

**Issue:** Authentication expired (after 90 days)

**Symptoms:** Logs show `401 Unauthorized` or `AADSTS50078`  
**Fix:**
```bash
# Delete cached token
rm ~/.cache/msal_token_cache.bin

# Re-authenticate
python3 -c "from shared.auth import get_graph_token; get_graph_token()"

# Follow device code flow prompts
```

---

### 4.6 Health Check Script

**Location:** `shared/healthcheck.sh`

**Run Weekly:**
```bash
cd /home/aaronshirley751/charter-and-stone-automation
bash shared/healthcheck.sh
```

**Checks Performed:**
- [ ] Service status (running/failed)
- [ ] Rclone mount accessibility
- [ ] Recent log errors (last 1 hour)
- [ ] Disk space on mount (warn if >80% full)
- [ ] Token expiration (warn if <7 days remaining)
- [ ] Last successful Teams notification (warn if >24 hours)

**Output:**
```
[✓] charterstone.service is active
[✓] Rclone mount is accessible
[!] Warning: 2 ERROR entries in last hour
[✓] Disk usage: 45% (safe)
[✓] Token expires in 62 days
[✓] Last Teams alert: 2 hours ago
```

---

## 5. OPERATIONAL NOTES

### 5.1 Power Management

**Pi 5 Power Loss Handling:**
- Service configured with `Restart=always` in systemd
- On unexpected shutdown, service auto-restarts on boot
- Rclone mount state does NOT persist across reboots
- First boot after power loss takes ~60 seconds (mount initialization)

**Planned Shutdowns:**
```bash
# Graceful shutdown (recommended)
sudo systemctl stop charterstone.service
sudo shutdown -h now

# Fast shutdown (emergency only)
sudo poweroff
```

---

### 5.2 Network Requirements

**Bandwidth:**
- Upload: ~10 Mbps (for large document syncs)
- Download: ~5 Mbps (for RSS feeds, 990 PDFs)

**Firewall Ports:**
- **Outbound 443 (HTTPS):** Required for all API calls
- **Outbound 53 (DNS):** Required for domain resolution

**Static IP Recommended:**
- Prevents DHCP lease conflicts on router reboots
- Set in `/etc/dhcpcd.conf` on Pi

---

### 5.3 Backup Strategy

**Critical Files to Backup (Daily):**
- `~/.cache/msal_token_cache.bin` (authentication)
- `agents/sentinel/.env` (configuration)
- `/etc/systemd/system/charterstone.service` (service definition)

**Automated Backup (via Rclone):**
```bash
# Add to crontab
0 3 * * * rclone sync ~/.cache/msal_token_cache.bin charterstone:Backups/tokens/
```

---

### 5.4 Monitoring & Alerts

**Current Setup:**
- Teams notifications for document processing
- No automated health monitoring yet

**Future Enhancements (Roadmap):**
- Dead Man's Switch: Alert if no activity for 6 hours
- Disk space alerts when mount >80% full
- Token expiration warnings at 7 days remaining

---

## 6. CONTACT & ESCALATION

**System Administrator:** Aaron Shirley  
**Escalation Path:**
1. Check logs: `journalctl -u charterstone -n 100`
2. Attempt service restart: `sudo systemctl restart charterstone.service`
3. If authentication errors: Re-run device code flow
4. If persistent failures: Post in Teams "#Tech-Support" channel

**Microsoft Support Contacts:**
- Graph API issues: https://aka.ms/graphsupport
- SharePoint sync issues: Submit ticket via M365 Admin Center

---

**END OF OPERATIONS MANUAL**
