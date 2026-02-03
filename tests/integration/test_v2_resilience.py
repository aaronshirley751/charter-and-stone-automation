from unittest.mock import patch
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.analyst.core import enhance_profile_with_v2_lite


def _build_v1_profile():
    return {
        "profile_version": "1.0.0",
        "university_name": "Test University",
        "ein": "12-3456789",
        "signals": {
            "pain_level": 80
        },
        "v1_signals": {
            "operating_deficit": -1000000,
            "pain_level": "SEVERE",
            "budget_capacity": 60,
            "decision_velocity": 70
        },
        "metadata": {
            "analyst_version": "1.1",
            "processing_timestamp": "2026-02-03T00:00:00Z"
        }
    }


def test_perplexity_failure_preserves_v1():
    v1_profile = _build_v1_profile()

    with patch("agents.analyst.core.orchestrator.execute_recon", side_effect=ConnectionError("API unavailable")):
        result = enhance_profile_with_v2_lite(
            v1_profile=v1_profile,
            university_name="Test University",
            ein="12-3456789",
            enable_v2=True
        )

    assert result == v1_profile


def test_claude_failure_preserves_v1():
    v1_profile = _build_v1_profile()

    with patch("agents.analyst.core.orchestrator.execute_recon", return_value={"raw_results": {}, "queries_executed": 3}):
        with patch("agents.analyst.core.orchestrator.extract_signals", side_effect=RuntimeError("Claude unavailable")):
            result = enhance_profile_with_v2_lite(
                v1_profile=v1_profile,
                university_name="Test University",
                ein="12-3456789",
                enable_v2=True
            )

    assert result == v1_profile
