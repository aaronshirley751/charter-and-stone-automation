"""Integration test: V1 legacy mode (V2 disabled)."""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
ANALYST_ROOT = PROJECT_ROOT / "agents" / "analyst"

for path in (str(PROJECT_ROOT), str(ANALYST_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from agents.analyst.analyst import generate_dossier


def _mock_financials():
    financial_data = {
        "filing_year": 2023,
        "total_revenue": 50000000,
        "total_expenses": 52000000,
        "total_assets": 75000000,
        "net_assets": 30000000,
        "tuition_revenue": 20000000,
        "contributions": 3000000,
        "investment_income": 1500000,
    }
    org_info = {
        "name": "Legacy Test University",
        "ein": "12-3456789",
        "city": "Testville",
        "state": "TX",
        "classification": "Baccalaureate College",
        "enrollment": 2500,
        "website": "https://example.edu",
    }
    return financial_data, org_info


@patch("sources.propublica.ProPublicaAPI.get_organization_financials")
def test_v1_legacy_mode_no_v2_signals(mock_get_financials, tmp_path: Path):
    """
    Ensure V1-only mode produces schema v1.0.0 without v2_signals.
    """
    mock_get_financials.return_value = _mock_financials()

    result_paths = generate_dossier(
        target_name="Legacy Test University",
        ein="12-3456789",
        output_dir=str(tmp_path),
        enable_v2_lite=False,
    )

    json_path = Path(result_paths["json"])
    assert json_path.exists(), "JSON profile output was not created"

    with json_path.open("r", encoding="utf-8") as handle:
        profile = json.load(handle)

    assert profile.get("meta", {}).get("schema_version") == "1.0.0"
    assert "v2_signals" not in profile
