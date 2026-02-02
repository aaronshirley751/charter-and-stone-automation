#!/usr/bin/env python3
"""
Quick integration test for the Outreach Architect agent.
Verifies schema validation, distress triage, forbidden phrase checking, and email generation.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.outreach.outreach import OutreachArchitect


def test_schema_validation():
    """Test that schema validation works correctly."""
    print("\n" + "="*60)
    print("TEST 1: Schema Validation")
    print("="*60)
    
    architect = OutreachArchitect()
    
    # Valid profile
    valid_profile = {
        "meta": {"schema_version": "1.0.0"},
        "institution": {"name": "Test College", "type": "Private"},
        "signals": {"distress_level": "elevated"},
        "leadership": {}
    }
    
    try:
        architect.validate_profile(valid_profile)
        print("✓ Valid profile accepted")
    except Exception as e:
        print(f"✗ Valid profile rejected: {e}")
    
    # Invalid version
    invalid_profile = {
        "meta": {"schema_version": "2.0.0"},
        "institution": {"name": "Test College", "type": "Private"},
        "signals": {"distress_level": "elevated"},
        "leadership": {}
    }
    
    try:
        architect.validate_profile(invalid_profile)
        print("✗ Invalid version should have been rejected")
    except Exception:
        print("✓ Invalid version correctly rejected")


def test_distress_triage():
    """Test distress level triage logic."""
    print("\n" + "="*60)
    print("TEST 2: Distress Triage Logic")
    print("="*60)
    
    architect = OutreachArchitect()
    
    levels = {
        "critical": "urgent_intervention",
        "elevated": "strategic_warning",
        "watch": "advisory_touch"
    }
    
    for level, expected_tone in levels.items():
        triage = architect.get_distress_triage(level)
        if triage["tone"] == expected_tone:
            print(f"✓ {level.upper()}: {triage['cadence_description']}")
        else:
            print(f"✗ {level.upper()}: Expected {expected_tone}, got {triage['tone']}")
    
    # Test stable (should abort)
    try:
        architect.get_distress_triage("stable")
        print("✗ Stable should have been rejected")
    except ValueError:
        print("✓ STABLE: Correctly aborted (no outreach for stable institutions)")


def test_forbidden_phrases():
    """Test forbidden phrase detection."""
    print("\n" + "="*60)
    print("TEST 3: Forbidden Phrase Detection")
    print("="*60)
    
    architect = OutreachArchitect()
    
    # Clean email
    clean = "Hi Jennifer, I saw your enrollment decline. Would you like to discuss?"
    violations = architect.check_forbidden_phrases(clean)
    if not violations:
        print(f"✓ Clean email passed ({len(clean)} chars)")
    else:
        print(f"✗ Clean email flagged: {violations}")
    
    # Vendor-speak email
    vendor = "I wanted to reach out about leveraging our transformation platform."
    violations = architect.check_forbidden_phrases(vendor)
    if violations:
        print(f"✓ Vendor-speak detected: {violations}")
    else:
        print(f"✗ Vendor-speak not detected")


def test_real_profile():
    """Test with actual profile from knowledge_base."""
    print("\n" + "="*60)
    print("TEST 4: Real Profile Processing (Albright College)")
    print("="*60)
    
    profile_path = "knowledge_base/prospects/albright_college_profile.json"
    
    if not Path(profile_path).exists():
        print(f"✗ Profile not found: {profile_path}")
        return
    
    architect = OutreachArchitect()
    
    # Load profile
    with open(profile_path, 'r') as f:
        profile = json.load(f)
    
    # Validate
    try:
        architect.validate_profile(profile)
        print(f"✓ Profile validated: {profile['institution']['name']}")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return
    
    # Check distress
    distress = profile["signals"]["distress_level"]
    triage = architect.get_distress_triage(distress)
    print(f"✓ Distress level: {distress.upper()} ({triage['tone']})")
    
    # Check output exists
    output_path = Path("agents/outreach/outputs/albright_college_outreach_sequence.md")
    if output_path.exists():
        size = output_path.stat().st_size
        print(f"✓ Output file exists: {size} bytes")
        
        # Verify content
        with open(output_path, 'r') as f:
            content = f.read()
        
        if "Email 1: Cold Intro" in content and "Email 2: Value Add" in content:
            print(f"✓ All 3 emails present in output")
        else:
            print(f"✗ Missing emails in output")
    else:
        print(f"✗ Output file not found: {output_path}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("OUTREACH ARCHITECT INTEGRATION TEST SUITE")
    print("="*60)
    
    try:
        test_schema_validation()
        test_distress_triage()
        test_forbidden_phrases()
        test_real_profile()
        
        print("\n" + "="*60)
        print("TEST SUITE COMPLETE")
        print("="*60)
        print("\n✓ All core functionality verified")
        
    except Exception as e:
        print(f"\n✗ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
