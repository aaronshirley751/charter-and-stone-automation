feat(sentinel): stabilize cloud sync and fix rclone corruption errors

Major stability overhaul for the Charter & Stone Sentinel automation pipeline.

**Changes:**
- **Service Hardening (`charterstone.service`):**
    - Added `ExecStartPre` cleanup to force unmount `fusermount -uz` before startup, preventing "zombie" process locks.
    - Updated `rclone mount` flags to strictly handle SharePoint metadata quirks:
        - Added `--ignore-checksum` and `--ignore-size` to prevent false positive "corruption" errors on .docx uploads.
        - Added `--no-modtime` to ignore timestamp drifts.
- **Race Condition Fix (`auto_publisher.py`):**
    - Injected 20s delay (`time.sleep`) post-processing to ensure Rclone upload completes before Teams notification triggers (fixing 404 errors).

**Status:** Commissioning complete. System is stable.