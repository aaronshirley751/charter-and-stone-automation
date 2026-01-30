"""
SHARED MEMORY MODULE
--------------------
Standardizes how agents save data to the Knowledge Base (The Oracle).
Ensures all knowledge is saved as standardized Markdown with metadata.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Define Root of Knowledge Base relative to this file
# (shared/memory.py -> ../knowledge_base)
KB_ROOT = Path(__file__).parent.parent / "knowledge_base"

def save_signal(title: str, content: str, signal_type: str = "distress", source_url: str = None, metadata: dict = None):
    """
    Saves an intelligence signal (from Watchdog) to the Knowledge Base.
    
    Args:
        title: Headline of the event
        content: Full text or summary
        signal_type: 'distress' or 'forecast'
        source_url: Where the intel came from
        metadata: Dict of extra info (university name, state, etc.)
    """
    # 1. Clean Title for Filename
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip().replace(" ", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{safe_title}.md"
    
    # 2. Determine Path
    # Default to 'distress' if unknown type
    subfolder = signal_type if signal_type in ['distress', 'forecast'] else 'distress'
    save_path = KB_ROOT / "signals" / subfolder / filename
    
    # 3. Construct Markdown Content
    md_content = f"""---
title: "{title}"
date: {datetime.now().isoformat()}
type: {signal_type}
source: {source_url or 'Unknown'}
metadata: {json.dumps(metadata or {})}
---

# {title}

**Source:** {source_url}
**Captured:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Intelligence Brief
{content}
"""

    # 4. Save
    _write_file(save_path, md_content)
    return str(save_path)

def save_document_text(filename: str, text_content: str, doc_type: str = "internal"):
    """
    Saves extracted text from a document (from Sentinel) to the KB.
    """
    # Strip extension from original filename
    base_name = Path(filename).stem
    save_name = f"{base_name}.md"
    
    save_path = KB_ROOT / "docs" / doc_type / save_name
    
    md_content = f"""---
original_file: "{filename}"
processed_date: {datetime.now().isoformat()}
type: document_extraction
---

# Document Extraction: {filename}

{text_content}
"""
    _write_file(save_path, md_content)
    return str(save_path)

def _write_file(path: Path, content: str):
    """Internal helper to write file safely."""
    try:
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write (UTF-8)
        path.write_text(content, encoding="utf-8")
        print(f"✅ [MEMORY] Saved to Oracle: {path.name}")
    except Exception as e:
        print(f"❌ [MEMORY] Failed to save {path.name}: {e}")
