import json
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.analyst.core import enhance_profile_with_v2_lite


def _build_v1_profile():
    return {
        "profile_version": "1.0.0",
        "university_name": "Albright College",
        "ein": "23-1352650",
        "signals": {
            "pain_level": 85
        },
        "v1_signals": {
            "operating_deficit": -20100000,
            "pain_level": "CRITICAL",
            "budget_capacity": 85,
            "decision_velocity": 92
        },
        "metadata": {
            "analyst_version": "1.1",
            "processing_timestamp": "2026-02-03T00:00:00Z"
        }
    }


@pytest.mark.integration
def test_albright_smoke():
    v1_profile = _build_v1_profile()

    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not perplexity_key:
        pytest.skip("PERPLEXITY_API_KEY not set — live API test skipped")
    if not anthropic_key:
        pytest.skip("ANTHROPIC_API_KEY not set — live API test skipped")

    enhanced = enhance_profile_with_v2_lite(
        v1_profile=v1_profile,
        university_name="Albright College",
        ein="23-1352650",
        enable_v2=True
    )

    print(json.dumps(enhanced, indent=2, ensure_ascii=False))

    v2_block = enhanced.get("v2_signals", {})

    assert v2_block, "v2_signals block missing"
    assert v2_block.get("composite_score", 0) >= 85
    assert v2_block.get("urgency_flag") in ["IMMEDIATE", "HIGH"]
    assert "real_time_intel" in v2_block
    assert v2_block["real_time_intel"].get("enrollment_trends")
    assert v2_block["real_time_intel"].get("leadership_changes")
    assert v2_block["real_time_intel"].get("accreditation_status")

    assert enhanced.get("metadata", {}).get("intelligence_queries_used") == 3
