# Charter & Stone Automation Server (Sentinel)

**Status:** ✅ Active Duty (Operation Sentinel)  
**System:** Raspberry Pi 5 (Headless / Silent Mode)

An automated document processing system that monitors a local folder for Markdown files, converts them into branded Word documents, and publishes notifications to Microsoft Teams via Power Automate Webhooks.

## Features

- **Automated Conversion:** Watches `src/_INBOX` for new `.md` files.
- **Branding:** Applies Charter & Stone styles using a reference Word template.
- **Reliable Cloud Sync:** Uses hardened `rclone` mount settings to interface with SharePoint.
- **Notifications:** Sends a rich Adaptive Card to Microsoft Teams with a direct link to the document.
- **Self-Healing:** Service includes "Breach and Clear" protocols to handle stale mounts and process locks.

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
    Create a `.env` file in the `src/` directory:

    ```ini
    TARGET_ROOT=/home/user/mountpoint/TargetFolder
    SHAREPOINT_FOLDER_URL=https://your-sharepoint-site/Shared%20Documents/TargetFolder
    TEAMS_WEBHOOK_URL=https://your-power-automate-webhook-url
    ```

4.  **Systemd Service (The "Golden Config"):**
    The `charterstone.service` file is critical for stability. It includes specific flags to handle SharePoint's metadata behavior:
    - `--vfs-cache-mode writes`: Delays upload until file close.
    - `--ignore-checksum` & `--no-checksum`: Prevents false "corruption" errors from SharePoint metadata modification.
    - `--ignore-size`: Ignores file size changes post-upload.
    - `--no-modtime`: Ignores timestamp drifts.

## Usage

The system runs as a background service (`charterstone.service`).

To manually trigger or test:
```bash
python src/auto_publisher.py
```

Drop a Markdown file into `src/_INBOX`. The system will:
1.  Detect the file.
2.  Convert to `.docx` with branding.
3.  Upload to SharePoint.
4.  Wait for sync (20s safety buffer).
5.  Post to Teams.

## Commissioning Log (Jan 26, 2026)

**Operation Sentinel** stabilized the pipeline with the following resolutions:

-   **Zombie Lock Fix:** Added `fusermount -uz` pre-start command to clear stale mounts.
-   **Ghost Drive Fix:** Enforced strict dependency ordering in systemd.
-   **Race Condition Fix:** Added tactical delay to `auto_publisher.py` to ensure upload completion before notification.
-   **SharePoint Compatibility:** Applied "Golden Flags" to `rclone` to ignore cloud-side metadata changes that caused file deletion/corruption errors.
