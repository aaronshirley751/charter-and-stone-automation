"""
Distress Signals Module
Mock implementation for V0.1 — will connect to SharePoint/Planner in future versions.
"""

from typing import List, Dict


def get_signals_for_target(target_name: str) -> List[Dict]:
    """
    Retrieve distress signals for a target institution.
    
    Args:
        target_name: Institution name
        
    Returns:
        List of signal dictionaries
        
    Note:
        V0.1 returns mock data. Future versions will query:
        - SharePoint lists
        - Microsoft Planner tasks
        - RSS feed aggregations
    """
    
    # Mock data for testing
    mock_signals = {
        "albright college": [
            {
                "date": "2025-01-15",
                "type": "FINANCIAL",
                "description": "Moody's downgraded credit rating to B2"
            },
            {
                "date": "2025-01-20",
                "type": "ENROLLMENT",
                "description": "Spring enrollment down 12% YoY"
            },
            {
                "date": "2025-01-28",
                "type": "LEADERSHIP",
                "description": "CFO resignation announced"
            }
        ]
    }
    
    # Normalize target name for lookup
    normalized_name = target_name.lower().strip()
    
    signals = mock_signals.get(normalized_name, [])
    
    print(f"[SIGNALS] Found {len(signals)} signal(s) for {target_name}")
    
    return signals