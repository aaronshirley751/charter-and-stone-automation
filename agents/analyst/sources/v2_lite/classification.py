"""
CLASSIFICATION MODULE: Composite V1+V2 Scoring Logic
Combines IRS 990 signals (V1) with real-time intelligence (V2) into unified urgency score.

Scoring Philosophy:
  - Base score from V1 (990 data): 0-100 representing financial distress
  - V2 amplification: Binary trust gates (TRUSTED sources only)
  - No weighted credibility: Only TRUSTED signals amplify score
  - Composite range: 0-100 (capped at 100)
  
Urgency Flags:
  - IMMEDIATE: Score >= 90 (crisis intervention required)
  - HIGH: Score 75-89 (active engagement recommended)
  - MONITOR: Score < 75 (watch for escalation)

Authorization: OPERATION_SNIPER_FINAL_AUTHORIZATION_V2_LITE.md
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone


def calculate_composite_score(
    v1_signals: Dict[str, Any],
    v2_signals: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate composite distress score from V1 and V2 signals.
    
    Args:
        v1_signals: Dictionary with V1 signals including 'pain_level' or 'pain_level_score'
        v2_signals: Dictionary with V2 signals (enrollment_trends, leadership_changes, accreditation_status)
        
    Returns:
        Dictionary with composite_score, urgency_flag, and v2_contribution metrics
    """
    
    # Extract base score from V1
    base_score = v1_signals.get('pain_level_score', v1_signals.get('pain_level', 0))
    
    # Handle string representations of pain_level (e.g., "CRITICAL")
    pain_level_map = {
        'CRITICAL': 85,
        'SEVERE': 75,
        'ELEVATED': 65,
        'MODERATE': 50,
        'LOW': 25,
        'MINIMAL': 10
    }
    
    if isinstance(base_score, str):
        base_score = pain_level_map.get(base_score.upper(), 50)
    
    base_score = max(0, min(100, float(base_score)))  # Clamp to 0-100
    
    # Initialize amplification tracker
    amplification = 0
    amplified_signals = []
    
    # Only amplify on TRUSTED signals
    
    # Signal 1: Enrollment Trends
    enrollment_signal = v2_signals.get('enrollment_trends', {})
    if enrollment_signal.get('credibility') == 'TRUSTED':
        finding = enrollment_signal.get('finding', '').lower()
        if any(word in finding for word in ['decline', 'drop', 'fell', 'decreased', 'loss', 'reduced']):
            amplification += 10
            amplified_signals.append({
                "signal": "enrollment_trends",
                "amplification": 10,
                "finding_snippet": enrollment_signal.get('finding', 'N/A')[:80]
            })
    
    # Signal 2: Leadership Changes
    leadership_signal = v2_signals.get('leadership_changes', {})
    if leadership_signal.get('credibility') == 'TRUSTED':
        finding = leadership_signal.get('finding', '').lower()
        if any(word in finding for word in ['interim', 'resignation', 'resigned', 'resigned', 'departure', 'departed', 'turnover']):
            amplification += 15
            amplified_signals.append({
                "signal": "leadership_changes",
                "amplification": 15,
                "finding_snippet": leadership_signal.get('finding', 'N/A')[:80]
            })
    
    # Signal 3: Accreditation & Regulatory
    accreditation_signal = v2_signals.get('accreditation_status', {})
    if accreditation_signal.get('credibility') == 'TRUSTED':
        finding = accreditation_signal.get('finding', '').lower()
        if any(word in finding for word in ['probation', 'warning', 'closure', 'alert', 'violation', 'sanction']):
            amplification += 20
            amplified_signals.append({
                "signal": "accreditation_status",
                "amplification": 20,
                "finding_snippet": accreditation_signal.get('finding', 'N/A')[:80]
            })
    
    # Calculate composite score (capped at 100)
    composite_score = min(base_score + amplification, 100)
    composite_score = int(composite_score)  # Convert to integer
    
    # Determine urgency flag
    if composite_score >= 90:
        urgency_flag = "IMMEDIATE"
    elif composite_score >= 75:
        urgency_flag = "HIGH"
    else:
        urgency_flag = "MONITOR"
    
    return {
        "composite_score": composite_score,
        "urgency_flag": urgency_flag,
        "v1_base_score": int(base_score),
        "v2_amplification": amplification,
        "amplified_signals": amplified_signals,
        "calculation_timestamp": datetime.now(timezone.utc).isoformat(),
        "scoring_model": "V2.0-LITE",
        "credibility_gates_applied": True
    }


def calculate_v2_lite_composite(
    v1_profile: Dict[str, Any],
    v2_signals_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Full pipeline composite calculation from V1 profile and V2 signals.
    Wraps calculate_composite_score with enhanced input handling.
    
    Args:
        v1_profile: Complete V1 profile with 'signals' key
        v2_signals_dict: Dictionary with enrollment_trends, leadership_changes, accreditation_status
        
    Returns:
        Enhanced scoring dictionary ready for profile merge
    """
    
    v1_signals = v1_profile.get('signals', v1_profile)
    
    composite_result = calculate_composite_score(
        v1_signals=v1_signals,
        v2_signals=v2_signals_dict
    )
    
    return {
        "composite_score": composite_result["composite_score"],
        "urgency_flag": composite_result["urgency_flag"],
        "v1_base_score": composite_result["v1_base_score"],
        "v2_contribution": composite_result["v2_amplification"],
        "signal_breakdown": composite_result["amplified_signals"],
        "calculation_timestamp": composite_result["calculation_timestamp"]
    }
