"""
Charter & Stone - Planner Task Janitor

Scans a Planner bucket for duplicate task titles and deletes the extras.
Keeps the first occurrence, removes subsequent duplicates.
"""

import sys
import os
import json
import requests
from dotenv import load_dotenv

# PATH SETUP: Add root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

# Import Shared Auth
from shared.auth import get_graph_headers

# Load env from root
load_dotenv(os.path.join(project_root, ".env"))

# =============================================================================
# CONFIGURATION
# =============================================================================

BUCKET_ID = "QDeSpyXMUUaBLf2cJIi84WUALZr_"  # Strategy & Intel bucket

# =============================================================================
# JANITOR LOGIC
# =============================================================================

def cleanup_duplicates():
    """
    Scan bucket for duplicate task titles and delete extras.
    Keeps first occurrence, deletes subsequent ones.
    """
    
    headers = get_graph_headers()
    if not headers:
        print("❌ Failed to authenticate. Cannot proceed.")
        return
    
    print(f"🧹 Janitor starting: Scanning bucket {BUCKET_ID}...")
    
    # 1. Get all tasks in the bucket
    url = f"https://graph.microsoft.com/v1.0/planner/buckets/{BUCKET_ID}/tasks"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tasks = response.json().get('value', [])
        print(f"📋 Found {len(tasks)} tasks in bucket.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to list tasks: {e}")
        return
    
    # 2. Track seen titles and identify duplicates
    seen_titles = {}
    duplicates = []
    
    for task in tasks:
        task_id = task.get('id')
        title = task.get('title', 'Untitled')
        
        if title in seen_titles:
            # This is a duplicate!
            duplicates.append({
                'id': task_id,
                'title': title,
                'original_id': seen_titles[title]['id']
            })
        else:
            # First occurrence - keep it
            seen_titles[title] = {
                'id': task_id,
                'title': title
            }
    
    if not duplicates:
        print("✅ No duplicates found. Bucket is clean!")
        return
    
    print(f"\n⚠️  Found {len(duplicates)} duplicate task(s):")
    for dup in duplicates:
        print(f"   - '{dup['title']}' (ID: {dup['id'][:8]}...)")
    
    # 3. Delete duplicates
    print(f"\n🗑️  Deleting duplicates...")
    deleted_count = 0
    
    for dup in duplicates:
        task_id = dup['id']
        title = dup['title']
        
        try:
            # First, fetch the task to get the ETag
            get_url = f"https://graph.microsoft.com/v1.0/planner/tasks/{task_id}"
            get_response = requests.get(get_url, headers=headers)
            get_response.raise_for_status()
            
            etag = get_response.headers.get('@odata.etag')
            if not etag:
                # Try getting it from the response body
                etag = get_response.json().get('@odata.etag')
            
            if not etag:
                print(f"   ⚠️  Could not get ETag for '{title}' - skipping")
                continue
            
            # Now delete with the ETag
            delete_headers = headers.copy()
            delete_headers['If-Match'] = etag
            
            delete_response = requests.delete(get_url, headers=delete_headers)
            delete_response.raise_for_status()
            print(f"   ✅ Deleted duplicate: '{title}'")
            deleted_count += 1
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Failed to delete '{title}': {e}")
    
    # 4. Summary
    print(f"\n{'='*60}")
    print(f"✅ Cleanup complete!")
    print(f"   - Duplicates deleted: {deleted_count}/{len(duplicates)}")
    print(f"   - Unique tasks remaining: {len(seen_titles)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    try:
        cleanup_duplicates()
    except KeyboardInterrupt:
        print("\n⏸️  Janitor interrupted by user.")
    except Exception as e:
        print(f"❌ Janitor error: {e}")
