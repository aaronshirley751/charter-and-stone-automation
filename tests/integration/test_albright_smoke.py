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


def _mock_execute_recon(university_name, ein, api_key=None):
    return {
        "raw_results": {
            "enrollment_financial": {
                "status": "success",
                "query": "mock",
                "response": {"results": []}
            },
            "leadership": {
                "status": "success",
                "query": "mock",
                "response": {"results": []}
            },
            "accreditation": {
                "status": "success",
                "query": "mock",
                "response": {"results": []}
            }
        },
        "queries_executed": 3,
        "queries_budget": 3,
        "university_name": university_name,
        "ein": ein,
        "timestamp": "2026-02-03T00:00:00Z"
    }


def _mock_extract_signals(raw_perplexity_results, university_name, api_key=None, system_prompt_path=None):
    return {
        "status": "success",
        "signals": {
            "enrollment_trends": {
                "finding": "15% enrollment decline Fall 2024",
                "source": "Inside Higher Ed, 2024-10-08",
                "credibility": "TRUSTED"
            },
            "leadership_changes": {
                "finding": "Interim CFO appointed January 2025",
                "source": "Campus announcement, 2025-01-15",
                "credibility": "TRUSTED"
            },
            "accreditation_status": {
                "finding": "MSCHE issued probation warning",
                "source": "MSCHE public disclosure, 2024-06-20",
                "credibility": "TRUSTED"
            }
        },
        "extraction_timestamp": "2026-02-03T00:00:00Z",
        "university_name": university_name,
        "model": "mock",
        "status": "success"
    }


def test_albright_smoke(monkeypatch):
    v1_profile = _build_v1_profile()

    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not perplexity_key or not anthropic_key:
        monkeypatch.setattr(
            "agents.analyst.core.orchestrator.execute_recon",
            _mock_execute_recon
        )
        monkeypatch.setattr(
            "agents.analyst.core.orchestrator.extract_signals",
            _mock_extract_signals
        )
        test_mode = "mocked"
    else:
        test_mode = "live"

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

    if test_mode == "mocked":
        assert enhanced.get("metadata", {}).get("intelligence_queries_used") == 3
