"""
Gate 2: 5-University Batch Test
CSO Directive: Prove V2-LITE provides differentiated scoring across distress spectrum

Test Cohort:
- Albright College (23-1352650) -> Expected: Critical (Baseline)
- Rockland Community College (13-1969305) -> Expected: High/Critical (Enrollment + Budget)
- Sweet Briar College (54-0505282) -> Expected: High (Historical Fragility)
- Hampshire College (04-2104307) -> Expected: High (Chronic Instability)
- Birmingham-Southern College (63-0373104) -> Expected: Critical (Closed/Liquidated)

Output: JSON summary with University Name, Composite Score, Urgency Flag, Key Signals Detected
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = str(Path(__file__).parent.parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from agents.analyst.core.orchestrator import enhance_profile_with_v2_lite


# Test cohort with expected outcomes
TEST_COHORT = [
    {
        "name": "Albright College",
        "ein": "23-1352650",
        "expected": "Critical"
    },
    {
        "name": "Rockland Community College",
        "ein": "13-1969305",
        "expected": "High/Critical"
    },
    {
        "name": "Sweet Briar College",
        "ein": "54-0505282",
        "expected": "High"
    },
    {
        "name": "Hampshire College",
        "ein": "04-2104307",
        "expected": "High"
    },
    {
        "name": "Birmingham-Southern College",
        "ein": "63-0373104",
        "expected": "Critical"
    }
]


def extract_signals(v2_signals: dict) -> list:
    """
    Extract key signal findings from v2_signals block.
    
    Args:
        v2_signals: The v2_signals dictionary from enhanced profile
        
    Returns:
        List of signal finding summaries
    """
    signals = []
    
    if not v2_signals:
        return signals
    
    real_time_intel = v2_signals.get('real_time_intel', {})
    
    if real_time_intel:
        if 'enrollment_trends' in real_time_intel:
            finding = real_time_intel['enrollment_trends'].get('finding', 'N/A')
            credibility = real_time_intel['enrollment_trends'].get('credibility', 'N/A')
            signals.append({
                "category": "Enrollment Trends",
                "finding": finding,
                "credibility": credibility
            })
        
        if 'leadership_changes' in real_time_intel:
            finding = real_time_intel['leadership_changes'].get('finding', 'N/A')
            credibility = real_time_intel['leadership_changes'].get('credibility', 'N/A')
            signals.append({
                "category": "Leadership Changes",
                "finding": finding,
                "credibility": credibility
            })
        
        if 'accreditation_status' in real_time_intel:
            finding = real_time_intel['accreditation_status'].get('finding', 'N/A')
            credibility = real_time_intel['accreditation_status'].get('credibility', 'N/A')
            signals.append({
                "category": "Accreditation Status",
                "finding": finding,
                "credibility": credibility
            })
    
    return signals


def run_batch_test():
    """
    Execute 5-university batch test with V2-LITE enhancement.
    
    Returns:
        List of test results with composite scores and urgency flags
    """
    print("\n" + "="*80)
    print("GATE 2: 5-UNIVERSITY BATCH TEST - V2.0-LITE VALIDATION")
    print("="*80)
    print(f"Execution Start: {datetime.now().isoformat()}")
    print(f"CSO Directive: Prove differentiated scoring across distress spectrum\n")
    
    results = []
    
    for idx, university in enumerate(TEST_COHORT, 1):
        name = university["name"]
        ein = university["ein"]
        expected = university["expected"]
        
        print(f"\n[{idx}/5] Testing: {name} (EIN: {ein})")
        print(f"      Expected Outcome: {expected}")
        print("      Status: Processing...", end="", flush=True)
        
        try:
            # Create a V1 profile with required signal structure
            v1_profile = {
                "profile_version": "1.0.0",
                "ein": ein,
                "name": name,
                "signals": {
                    "distress_level_score": 50,  # Mid-range baseline
                    "distress_level": "watch"
                },
                "composite_score": 50,
                "distress_level": "watch"
            }
            
            # Run V2-LITE enhancement with proper arguments
            enhanced = enhance_profile_with_v2_lite(v1_profile, name, ein, enable_v2=True)
            
            if enhanced is None or enhanced.get('status') == 'error':
                print("\r" + " "*60 + "\r", end="")
                print(f"      Status: ERROR - V2 enhancement failed")
                result = {
                    "name": name,
                    "ein": ein,
                    "expected": expected,
                    "composite_score": None,
                    "urgency_flag": "ERROR",
                    "key_signals": [],
                    "status": "FAILED"
                }
            else:
                print("\r" + " "*60 + "\r", end="")
                
                composite_score = enhanced.get('composite_score', 0)
                urgency_flag = enhanced.get('urgency_flag', 'UNKNOWN')
                v2_signals = enhanced.get('v2_signals', {})
                key_signals = extract_signals(v2_signals)
                
                print(f"      Status: SUCCESS ✓")
                print(f"      Composite Score: {composite_score}")
                print(f"      Urgency Flag: {urgency_flag}")
                
                if key_signals:
                    print(f"      Key Signals Detected:")
                    for signal in key_signals:
                        cred_indicator = "✓ TRUSTED" if signal['credibility'] == "TRUSTED" else f"({signal['credibility']})"
                        print(f"        • {signal['category']}: {signal['finding'][:60]}... {cred_indicator}")
                
                result = {
                    "name": name,
                    "ein": ein,
                    "expected": expected,
                    "composite_score": composite_score,
                    "urgency_flag": urgency_flag,
                    "key_signals": [
                        {
                            "category": s['category'],
                            "finding": s['finding'],
                            "credibility": s['credibility']
                        }
                        for s in key_signals
                    ],
                    "status": "PASSED"
                }
            
            results.append(result)
        
        except Exception as e:
            print("\r" + " "*60 + "\r", end="")
            print(f"      Status: EXCEPTION - {str(e)}")
            result = {
                "name": name,
                "ein": ein,
                "expected": expected,
                "composite_score": None,
                "urgency_flag": "ERROR",
                "key_signals": [],
                "status": "EXCEPTION",
                "error": str(e)
            }
            results.append(result)
    
    return results


def validate_results(results: list) -> dict:
    """
    Validate batch test results against expectations.
    
    Args:
        results: List of test results
        
    Returns:
        Validation summary
    """
    passed = sum(1 for r in results if r['status'] == 'PASSED')
    failed = len(results) - passed
    
    # Check differentiation: verify scores are not all the same
    scores = [r['composite_score'] for r in results if r['composite_score'] is not None]
    score_diversity = len(set(scores)) > 1 if scores else False
    
    # Check urgency flags show variation
    urgency_flags = set(r['urgency_flag'] for r in results if r['urgency_flag'] != 'ERROR')
    flag_variation = len(urgency_flags) > 1
    
    # Check all results have signals (if passed)
    results_with_signals = sum(1 for r in results if r['status'] == 'PASSED' and r['key_signals'])
    
    validation = {
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "pass_rate": f"{(passed/len(results)*100):.1f}%" if results else "N/A",
        "score_differentiation": score_diversity,
        "urgency_variation": flag_variation,
        "results_with_signals": results_with_signals,
        "test_quality": "PASSED" if passed == len(results) and score_diversity and flag_variation else "REVIEW"
    }
    
    return validation


def main():
    """Execute batch test and output results."""
    
    # Run batch test
    results = run_batch_test()
    
    # Validate results
    validation = validate_results(results)
    
    # Print JSON output
    print("\n" + "="*80)
    print("BATCH TEST RESULTS (JSON)")
    print("="*80)
    
    output = {
        "test_name": "Gate 2: 5-University Batch Test",
        "execution_timestamp": datetime.now().isoformat(),
        "validation_summary": validation,
        "results": results
    }
    
    print(json.dumps(output, indent=2))
    
    # Print validation summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"Total Tests: {validation['total_tests']}")
    print(f"Passed: {validation['passed']}")
    print(f"Failed: {validation['failed']}")
    print(f"Pass Rate: {validation['pass_rate']}")
    print(f"Score Differentiation: {'✓ YES' if validation['score_differentiation'] else '✗ NO'}")
    print(f"Urgency Flag Variation: {'✓ YES' if validation['urgency_variation'] else '✗ NO'}")
    print(f"Results with Signals: {validation['results_with_signals']}/{validation['passed']}")
    print(f"Overall Test Quality: {validation['test_quality']}")
    
    # Print summary table
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS")
    print("="*80)
    print(f"{'University':<30} {'Score':<8} {'Urgency':<12} {'Expected':<12}")
    print("-"*80)
    for result in results:
        score = result['composite_score'] if result['composite_score'] is not None else "ERROR"
        urgency = result['urgency_flag']
        expected = result['expected']
        name = result['name'][:28]
        print(f"{name:<30} {str(score):<8} {urgency:<12} {expected:<12}")
    
    print("\n" + "="*80)
    print(f"Execution Complete: {datetime.now().isoformat()}")
    print("="*80)
    
    # Return exit code based on results
    return 0 if validation['test_quality'] == 'PASSED' else 1


if __name__ == "__main__":
    exit(main())
