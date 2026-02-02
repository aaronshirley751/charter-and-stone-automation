#!/usr/bin/env python3
"""
Charter & Stone — Deep Dive Analyst Agent V1.1
Generates comprehensive university dossiers from financial data and signals.

UPGRADE NOTES (V1.1):
- Dual output: Markdown dossier + JSON profile
- JSON output conforms to Prospect Data Standard schema v1.0.0
- Calculated metrics: expense_ratio, runway_years, tuition_dependency
- Blinded presentation block for external use
- Null-safety fixes applied per peer review

Usage:
    python3 analyst.py --target "University Name" --ein "12-3456789"
    python3 analyst.py --target "Albright College" --ein "23-1352607"
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Any

# Import data sources
from sources.propublica import ProPublicaAPI
from sources.signals import get_signals_for_target


# =============================================================================
# CONFIGURATION
# =============================================================================

AGENT_VERSION = "analyst-v1.1"
SCHEMA_VERSION = "1.0.0"

# Output directories (relative to user home)
DEFAULT_OUTPUT_BASE = Path.home() / "charter_stone" / "knowledge_base" / "prospects"

# State mappings for region detection
STATE_TO_REGION = {
    # Northeast
    "CT": "northeast", "ME": "northeast", "MA": "northeast", "NH": "northeast",
    "RI": "northeast", "VT": "northeast", "NJ": "northeast", "NY": "northeast",
    "PA": "northeast", "DE": "northeast", "MD": "northeast", "DC": "northeast",
    # Southeast
    "AL": "southeast", "AR": "southeast", "FL": "southeast", "GA": "southeast",
    "KY": "southeast", "LA": "southeast", "MS": "southeast", "NC": "southeast",
    "SC": "southeast", "TN": "southeast", "VA": "southeast", "WV": "southeast",
    # Midwest
    "IL": "midwest", "IN": "midwest", "IA": "midwest", "KS": "midwest",
    "MI": "midwest", "MN": "midwest", "MO": "midwest", "NE": "midwest",
    "ND": "midwest", "OH": "midwest", "SD": "midwest", "WI": "midwest",
    # Southwest
    "AZ": "southwest", "NM": "southwest", "OK": "southwest", "TX": "southwest",
    # West
    "AK": "west", "CA": "west", "CO": "west", "HI": "west", "ID": "west",
    "MT": "west", "NV": "west", "OR": "west", "UT": "west", "WA": "west",
    "WY": "west",
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def sanitize_filename(name: str) -> str:
    """Convert university name to valid filename."""
    return name.lower().replace(' ', '_').replace(',', '').replace('.', '').replace("'", '')


def format_ein(ein: str) -> str:
    """Ensure EIN is in XX-XXXXXXX format."""
    ein_clean = ein.replace('-', '').replace(' ', '')
    if len(ein_clean) == 9:
        return f"{ein_clean[:2]}-{ein_clean[2:]}"
    return ein


def fmt_currency(value: float) -> str:
    """Format number as currency string."""
    if value is None:
        return "N/A"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:,.0f}"


def get_region(state: str) -> str:
    """Get region from state code."""
    return STATE_TO_REGION.get(state.upper(), "unknown")


def generate_blinded_name(org_type: str, region: str) -> str:
    """Generate anonymized display name for external use."""
    type_map = {
        "private-nonprofit": "Private Nonprofit College",
        "private-forprofit": "Private For-Profit Institution",
        "public-state": "Public State University",
        "public-local": "Public Community College",
        "public-federal": "Federal Institution",
    }
    type_str = type_map.get(org_type, "Higher Education Institution")
    region_str = region.capitalize() if region != "unknown" else "United States"
    return f"Representative {type_str} ({region_str})"


def determine_distress_level(expense_ratio: float, runway_years: Optional[float], signals: list) -> str:
    """Determine overall distress level based on financial metrics and signals."""
    critical_signals = sum(1 for s in signals if s.get('severity') == 'critical')
    warning_signals = sum(1 for s in signals if s.get('severity') == 'warning')
    
    # Critical: Deficit spending >120% OR runway < 2 years OR 2+ critical signals
    if expense_ratio and expense_ratio > 1.2 or (runway_years and runway_years < 2) or critical_signals >= 2:
        return "critical"
    
    # Elevated: Deficit spending OR runway < 4 years OR 1 critical signal
    if expense_ratio and expense_ratio > 1.0 or (runway_years and runway_years < 4) or critical_signals >= 1:
        return "elevated"
    
    # Watch: Borderline metrics OR warning signals
    if expense_ratio and expense_ratio > 0.95 or warning_signals >= 2:
        return "watch"
    
    return "stable"


# =============================================================================
# JSON PROFILE GENERATION (Schema v1.0.0) - WITH NULL SAFETY FIXES
# =============================================================================

def build_profile_json(
    target_name: str,
    ein: str,
    financial_data: Dict[str, Any],
    signals: list,
    org_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build JSON profile conforming to Prospect Data Standard schema v1.0.0.
    
    PEER REVIEW FIXES APPLIED:
    - Bug #1: Null-safe expense_ratio calculation
    - Bug #2: Null-safe runway_years calculation  
    - Bug #3: Null-safe tuition_dependency calculation (handles 0 correctly)
    
    Args:
        target_name: Institution name
        ein: Employer Identification Number
        financial_data: Data from ProPublica API
        signals: List of distress/opportunity signals
        org_info: Organization metadata from API
        
    Returns:
        Complete profile dict ready for JSON serialization
    """
    now = datetime.now(timezone.utc).isoformat()
    ein_formatted = format_ein(ein)
    
    # Extract financial values (with safe defaults using 'or 0' pattern)
    total_revenue = financial_data.get('total_revenue') or 0
    total_expenses = financial_data.get('total_expenses') or 0
    net_assets = financial_data.get('net_assets') or 0
    fiscal_year = financial_data.get('filing_year', datetime.now().year - 1)
    
    # Calculate derived metrics
    operating_surplus_deficit = total_revenue - total_expenses
    
    # BUG FIX #1: Expense ratio (expenses / revenue) - NULL SAFETY
    if total_revenue > 0 and total_expenses is not None:
        expense_ratio = round(total_expenses / total_revenue, 3)
    else:
        expense_ratio = None
    
    # BUG FIX #2: Runway years (only if deficit) - NULL SAFETY
    if operating_surplus_deficit < 0 and net_assets > 0:
        annual_deficit = abs(operating_surplus_deficit)
        runway_years = round(net_assets / annual_deficit, 1)
    else:
        runway_years = None
    
    # BUG FIX #3: Tuition dependency - NULL SAFETY (handles 0 correctly)
    tuition_revenue = financial_data.get('tuition_revenue')
    if tuition_revenue is not None and total_revenue > 0:
        tuition_dependency = round(tuition_revenue / total_revenue, 3)
    else:
        tuition_dependency = None
    
    # Determine institution type and region
    state = org_info.get('state', '')
    region = get_region(state)
    
    # Default to private-nonprofit for higher ed (most common)
    org_type = "private-nonprofit"
    
    # Build signals array for schema
    schema_signals = []
    for sig in signals:
        schema_signals.append({
            "type": sig.get('type', 'news'),
            "signal": sig.get('description', ''),
            "severity": sig.get('severity', 'info'),
            "detected_at": sig.get('date', now),
            "source_url": sig.get('url')
        })
    
    # Determine distress level
    distress_level = determine_distress_level(
        expense_ratio or 0,
        runway_years,
        schema_signals
    )
    
    # Build the complete profile
    profile = {
        "meta": {
            "schema_version": SCHEMA_VERSION,
            "generated_at": now,
            "generated_by": AGENT_VERSION,
            "data_sources": [
                {
                    "source": "ProPublica Nonprofit Explorer",
                    "retrieved_at": now,
                    "confidence": "high"
                }
            ]
        },
        
        "institution": {
            "name": target_name,
            "aliases": [],
            "ein": ein_formatted,
            "type": org_type,
            "classification": org_info.get('classification'),
            "location": {
                "city": org_info.get('city'),
                "state": state,
                "region": region
            },
            "enrollment": {
                "total": org_info.get('enrollment'),
                "fte": None,
                "as_of": None
            },
            "website": org_info.get('website')
        },
        
        "financials": {
            "fiscal_year": fiscal_year,
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "operating_surplus_deficit": operating_surplus_deficit,
            "net_assets": net_assets,
            "tuition_revenue": tuition_revenue,
            "contributions": financial_data.get('contributions'),
            "investment_income": financial_data.get('investment_income'),
            "calculated": {
                "expense_ratio": expense_ratio,
                "runway_years": runway_years,
                "tuition_dependency": tuition_dependency
            },
            "data_source": {
                "form": "IRS-990",
                "tax_period": str(fiscal_year),
                "retrieved_from": "ProPublica Nonprofit Explorer API"
            }
        },
        
        "signals": {
            "distress_level": distress_level,
            "indicators": schema_signals,
            "news_hits": []  # Populated by Watchdog agent
        },
        
        "leadership": {
            "president": {
                "name": None,
                "title": None,
                "tenure_start": None,
                "email": None
            },
            "cfo": {
                "name": None,
                "title": None,
                "email": None
            },
            "provost": {
                "name": None,
                "title": None,
                "email": None
            },
            "stability_notes": None
        },
        
        "engagement": {
            "status": "prospect",
            "priority": "tier-2",
            "last_contact": None,
            "next_action": "Review diagnostic and determine outreach approach",
            "next_action_date": None,
            "owner": "unassigned",
            "notes": []
        },
        
        "blinded_presentation": {
            "display_name": generate_blinded_name(org_type, region),
            "approved_for_external": False
        }
    }
    
    return profile


# =============================================================================
# MARKDOWN DOSSIER GENERATION (V1.0 format preserved + enhancements)
# =============================================================================

def format_signals_markdown(signals: list) -> str:
    """Format signals list for markdown output."""
    if not signals:
        return "*(No active distress signals detected)*"
    
    output = []
    for signal in signals:
        severity_icon = {
            'critical': '🔴',
            'warning': '🟡',
            'info': '🔵'
        }.get(signal.get('severity', 'info'), '⚪')
        
        date_str = signal.get('date', 'Unknown date')
        sig_type = signal.get('type', 'Signal')
        description = signal.get('description', 'No description')
        
        output.append(f"- {severity_icon} **{date_str}** — {sig_type}: {description}")
    
    return "\n".join(output)


def generate_markdown_dossier(
    target_name: str,
    ein: str,
    financial_data: Dict[str, Any],
    signals: list,
    profile: Dict[str, Any]
) -> str:
    """
    Generate markdown dossier (human-readable format).
    
    Args:
        target_name: Institution name
        ein: Employer Identification Number  
        financial_data: Data from ProPublica API
        signals: List of distress signals
        profile: The JSON profile (for calculated values)
        
    Returns:
        Markdown string
    """
    # Extract values with null safety
    filing_year = financial_data.get('filing_year', 'Unknown')
    total_revenue = financial_data.get('total_revenue') or 0
    total_expenses = financial_data.get('total_expenses') or 0
    net_assets = financial_data.get('net_assets') or 0
    operating_result = total_revenue - total_expenses
    
    # Get calculated values from profile
    calculated = profile.get('financials', {}).get('calculated', {})
    expense_ratio = calculated.get('expense_ratio')
    runway_years = calculated.get('runway_years')
    distress_level = profile.get('signals', {}).get('distress_level', 'unknown')
    
    # Determine health status display
    if distress_level == 'critical':
        health_status = "🔴 CRITICAL"
    elif distress_level == 'elevated':
        health_status = "🟡 ELEVATED RISK"
    elif distress_level == 'watch':
        health_status = "🟡 WATCH"
    else:
        health_status = "🟢 STABLE"
    
    # Build dossier
    dossier = f"""# Prospect Dossier: {target_name}

---

| Field | Value |
|-------|-------|
| **Generated** | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |
| **Agent** | {AGENT_VERSION} |
| **EIN** | {format_ein(ein)} |
| **Data Source** | IRS Form 990 ({filing_year}) |

---

## Executive Summary

**Institution:** {target_name}  
**Health Status:** {health_status}  
**Distress Level:** {distress_level.upper()}

---

## Financial Overview (FY{filing_year})

| Metric | Value |
|--------|-------|
| **Total Revenue** | {fmt_currency(total_revenue)} |
| **Total Expenses** | {fmt_currency(total_expenses)} |
| **Operating Result** | {fmt_currency(operating_result)} |
| **Net Assets** | {fmt_currency(net_assets)} |

### Calculated Indicators

| Indicator | Value | Interpretation |
|-----------|-------|----------------|
| **Expense Ratio** | {f"{expense_ratio:.1%}" if expense_ratio else "N/A"} | {"⚠️ Deficit spending" if expense_ratio and expense_ratio > 1.0 else "✓ Within budget" if expense_ratio else "—"} |
| **Runway (Years)** | {f"{runway_years:.1f}" if runway_years else "N/A"} | {"🔴 Critical (<2 years)" if runway_years and runway_years < 2 else "🟡 Limited (<4 years)" if runway_years and runway_years < 4 else "—" if runway_years else "No deficit"} |

---

## Distress Signals

{format_signals_markdown(signals)}

---

## Engagement Recommendation

Based on the financial profile and signal analysis:

"""
    
    # Add recommendation based on distress level
    if distress_level == 'critical':
        dossier += """**PRIORITY: HIGH**

This institution shows critical financial distress indicators. Immediate outreach recommended with emphasis on:
- Operational triage services
- Financial stabilization consulting
- Leadership advisory support

*Suggested approach: Direct executive contact with diagnostic in hand.*
"""
    elif distress_level == 'elevated':
        dossier += """**PRIORITY: MEDIUM-HIGH**

This institution shows elevated risk indicators. Proactive outreach recommended with emphasis on:
- Financial health assessment
- Operational efficiency review
- Strategic planning support

*Suggested approach: Consultative outreach positioning Charter & Stone as a strategic partner.*
"""
    elif distress_level == 'watch':
        dossier += """**PRIORITY: MEDIUM**

This institution shows early warning indicators. Monitor and consider outreach with emphasis on:
- Preventive assessment
- Peer benchmarking
- Process optimization

*Suggested approach: Add to watch list; consider outreach if additional signals emerge.*
"""
    else:
        dossier += """**PRIORITY: LOW**

This institution appears financially stable. No immediate outreach recommended unless:
- Strategic opportunity identified
- Referral received
- New distress signals emerge

*Suggested approach: Monitor only.*
"""
    
    dossier += f"""
---

## Blinded Presentation

For use in external materials (pitch decks, case studies):

> **{profile.get('blinded_presentation', {}).get('display_name', 'Representative Institution')}**
> 
> - Operating deficit: {fmt_currency(operating_result) if operating_result < 0 else "None"}
> - Expense ratio: {f"{expense_ratio:.0%}" if expense_ratio else "N/A"}
> - Runway: {f"{runway_years:.1f} years" if runway_years else "N/A"}

*Note: External use requires `approved_for_external: true` in profile.json*

---

## Data Provenance

- **Source:** ProPublica Nonprofit Explorer API
- **Form:** IRS 990 (Tax Year {filing_year})
- **Retrieved:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Confidence:** High (official IRS filing data)

---

*This dossier was generated automatically by the Charter & Stone Analyst Agent.*
*Schema Version: {SCHEMA_VERSION}*
"""
    
    return dossier


# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================


def generate_dossier(target_name: str, ein: str, output_dir: str = None) -> Dict[str, str]:
    """
    Generate complete dossier package for a target institution.
    
    V1.1 UPGRADE: Dual output format
    1. Markdown dossier (human-readable)
    2. JSON profile (machine-readable, schema-compliant)
    
    Args:
        target_name: Official institution name
        ein: Employer Identification Number (format: XX-XXXXXXX)
        output_dir: Optional output directory path
        
    Returns:
        Dict with paths: {'markdown': path, 'json': path, 'elapsed_seconds': float}
    """
    start_time = datetime.now()
    
    print(f"[ANALYST] ══════════════════════════════════════════════════")
    print(f"[ANALYST] Charter & Stone — Deep Dive Analyst Agent {AGENT_VERSION}")
    print(f"[ANALYST] ══════════════════════════════════════════════════")
    print(f"[ANALYST] Target: {target_name}")
    print(f"[ANALYST] EIN: {format_ein(ein)}")
    print(f"[ANALYST] Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[ANALYST] ──────────────────────────────────────────────────")
    
    # Initialize API client
    api = ProPublicaAPI()
    
    # Fetch financial data
    print("[ANALYST] Fetching ProPublica data...")
    try:
        # Support both tuple return (financial_data, org_info) and dict return
        api_result = api.get_organization_financials(ein)
        if isinstance(api_result, tuple):
            financial_data, org_info = api_result
        else:
            # Legacy single return - extract org_info from financial_data
            financial_data = api_result
            org_info = {
                'city': financial_data.get('city'),
                'state': financial_data.get('state'),
                'classification': financial_data.get('classification'),
                'enrollment': financial_data.get('enrollment'),
                'website': financial_data.get('website')
            }
    except Exception as e:
        print(f"[ERROR] API request failed: {e}")
        sys.exit(1)
    
    if not financial_data:
        print("[ERROR] No financial data found. Check EIN and API status.")
        sys.exit(1)
    
    print(f"[ANALYST] ✓ Financial data retrieved (FY{financial_data.get('filing_year', '?')})")
    
    # Fetch signals
    print("[ANALYST] Fetching distress signals...")
    signals = get_signals_for_target(target_name)
    print(f"[ANALYST] ✓ {len(signals)} signal(s) retrieved")
    
    # Build JSON profile (schema-compliant)
    print("[ANALYST] Building JSON profile (schema v1.0.0)...")
    profile = build_profile_json(
        target_name=target_name,
        ein=ein,
        financial_data=financial_data,
        signals=signals,
        org_info=org_info
    )
    print(f"[ANALYST] ✓ Profile built (distress_level: {profile['signals']['distress_level']})")
    
    # Generate markdown dossier
    print("[ANALYST] Generating markdown dossier...")
    markdown_content = generate_markdown_dossier(
        target_name=target_name,
        ein=ein,
        financial_data=financial_data,
        signals=signals,
        profile=profile
    )
    print("[ANALYST] ✓ Markdown dossier generated")
    
    # Determine output paths
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_BASE
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # File naming: use EIN for JSON (unique), name for markdown (readable)
    ein_clean = ein.replace('-', '').replace(' ', '')
    json_filename = f"{ein_clean}_profile.json"
    md_filename = f"{sanitize_filename(target_name)}_dossier.md"
    
    json_path = output_dir / json_filename
    md_path = output_dir / md_filename
    
    # Write JSON profile
    print(f"[ANALYST] Writing JSON: {json_path}")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    # Write markdown dossier
    print(f"[ANALYST] Writing Markdown: {md_path}")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    # Calculate elapsed time
    elapsed = (datetime.now() - start_time).total_seconds()
    
    print(f"[ANALYST] ──────────────────────────────────────────────────")
    print(f"[ANALYST] ✓ COMPLETE in {elapsed:.2f} seconds")
    print(f"[ANALYST] ══════════════════════════════════════════════════")
    
    return {
        'markdown': str(md_path),
        'json': str(json_path),
        'elapsed_seconds': elapsed
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate university dossier + JSON profile from financial data"
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Institution name (e.g., 'Albright College')"
    )
    parser.add_argument(
        "--ein",
        required=True,
        help="EIN in format XX-XXXXXXX"
    )
    parser.add_argument(
        "--output",
        help="Custom output directory (optional)"
    )
    
    args = parser.parse_args()
    
    # Generate dossier package
    paths = generate_dossier(
        target_name=args.target,
        ein=args.ein,
        output_dir=args.output
    )
    
    print(f"\n📄 Markdown Dossier: {paths['markdown']}")
    print(f"📊 JSON Profile:     {paths['json']}")
    print(f"⏱️  Elapsed Time:     {paths['elapsed_seconds']:.2f}s")


if __name__ == "__main__":
    main()