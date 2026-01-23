# Charter & Stone Automation Server

An automated document processing system that monitors a local folder for Markdown files, converts them into branded Word documents, and publishes notifications to Microsoft Teams via Power Automate Webhooks.

## Features

- **Automated Conversion:** Watches `src/_INBOX` for new `.md` files.
- **Branding:** Applies Charter & Stone styles using a reference Word template.
- **Publishing:** Saves the final document to a synced SharePoint folder.
- **Notifications:** Sends a rich Adaptive Card to Microsoft Teams with a direct link to the document.

## Setup

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
    Create a `.env` file in the root directory with the following variables:

    ```ini
    TARGET_ROOT=path/to/your/synced/folder
    SHAREPOINT_FOLDER_URL=https://your-sharepoint-site/Shared%20Documents/YourFolder
    TEAMS_WEBHOOK_URL=https://your-power-automate-webhook-url
    ```

## Usage

Run the automation server:

```bash
python src/auto_publisher.py
```

The server will start monitoring the `src/_INBOX` folder. Simply drop a Markdown file into that folder to trigger the workflow.


## Recent Updates (Jan 23, 2026)

- **Security Improvements:** Refactored project to use `.env` file for sensitive configuration (Webhooks, Paths), removing hardcoded secrets from source code.
- **Workflow Enhancements:** Updated Microsoft Teams notifications to use direct Word Online links (`?web=1`) for one-click editing.
- **Path Handling:** Fixed Windows path syntax issues in configuration and path resolution.
- **Project Structure:** Added `.gitignore` and updated `requirements.txt` for better project hygiene.

