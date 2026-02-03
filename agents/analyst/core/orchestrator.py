"""
ORCHESTRATOR MODULE: Analyst V2.0-LITE Master Pipeline
Coordinates V1 (IRS 990) and V2 (real-time intelligence) analysis.

Orchestration Flow:
  Phase 1-4: V1 pipeline (existing 990 analysis)
  Phase 5: V2-LITE real-time intelligence layer (NEW)
  Phase 6: Composite scoring and profile merge

Authorization: OPERATION_SNIPER_FINAL_AUTHORIZATION_V2_LITE.md
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone

# Add parent directories to path for imports
current_dir = Path(__file__).parent
analyst_dir = current_dir.parent
agents_dir = analyst_dir.parent
project_root = agents_dir.parent
sys.path.insert(0, str(project_root))

# Import V2-LITE modules
from agents.analyst.sources.v2_lite import (
    execute_recon,
    extract_signals,
    calculate_composite_score
)


class AnalystV2Orchestrator:
    """
    Master orchestrator for V2.0-LITE pipeline.
    Manages Phase 5-6: Real-time intelligence and composite scoring.
    """
    
    def __init__(self, enable_v2_lite: bool = True):
        """
        Initialize orchestrator.
        
        Args:
            enable_v2_lite: Toggle V2-LITE features on/off (default: enabled)
        """
        self.enable_v2_lite = enable_v2_lite
        self.system_prompt_path = (
            analyst_dir / "config" / "prompts" / "synthesis_v2.txt"
        )
    
    def run_v2_lite_recon(self, university_name: str, ein: str) -> Dict[str, Any]:
        """
        Phase 5: Execute real-time intelligence reconnaissance.
        
        Args:
            university_name: Full university name
            ein: Employer Identification Number
            
        Returns:
            Raw reconnaissance results from 3 Perplexity queries
        """
        if not self.enable_v2_lite:
            return {
                "status": "skipped",
                "reason": "V2-LITE disabled",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        try:
            recon_results = execute_recon(
                university_name=university_name,
                ein=ein,
                api_key=os.environ.get('PERPLEXITY_API_KEY')
            )
            return recon_results
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def run_signal_extraction(
        self,
        raw_recon_results: Dict[str, Any],
        university_name: str
    ) -> Dict[str, Any]:
        """
        Phase 5b: Extract structured signals from raw reconnaissance.
        
        Args:
            raw_recon_results: Output from run_v2_lite_recon()
            university_name: Full university name
            
        Returns:
            Dictionary with extracted signals and metadata
        """
        if not self.enable_v2_lite:
            return {"status": "skipped"}
        
        try:
            # Extract just the raw_results for Claude processing
            raw_results = raw_recon_results.get('raw_results', {})
            
            extraction_result = extract_signals(
                raw_perplexity_results=raw_results,
                university_name=university_name,
                api_key=os.environ.get('ANTHROPIC_API_KEY'),
                system_prompt_path=str(self.system_prompt_path) if self.system_prompt_path.exists() else None
            )
            
            return extraction_result
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "signals": self._get_null_signals(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def run_composite_scoring(
        self,
        v1_profile: Dict[str, Any],
        v2_signals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Phase 6: Calculate composite score from V1 + V2 signals.
        
        Args:
            v1_profile: Complete V1 profile with 'signals' key
            v2_signals: Dictionary with enrollment_trends, leadership_changes, accreditation_status
            
        Returns:
            Composite scoring results with urgency flag
        """
        if not self.enable_v2_lite:
            return {"status": "skipped"}
        
        try:
            v1_signals = v1_profile.get('signals', v1_profile)
            
            composite_result = calculate_composite_score(
                v1_signals=v1_signals,
                v2_signals=v2_signals
            )
            
            return composite_result
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def merge_v2_into_profile(
        self,
        v1_profile: Dict[str, Any],
        raw_recon: Dict[str, Any],
        extracted_signals: Dict[str, Any],
        composite_score: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge V2-LITE results into V1 profile for backward-compatible output.
        
        Args:
            v1_profile: Original V1 profile
            raw_recon: Raw reconnaissance results
            extracted_signals: Extracted signals from Claude
            composite_score: Composite scoring results
            
        Returns:
            Enhanced profile with v2_signals block
        """
        if not self.enable_v2_lite:
            return v1_profile

        if raw_recon.get('status') == 'error' or extracted_signals.get('status') == 'error':
            return v1_profile
        
        # Extract signals from extraction result
        if extracted_signals.get('status') == 'error':
            signals_block = self._get_null_signals()
        else:
            signals_block = extracted_signals.get('signals', self._get_null_signals())
        
        # Build V2 signals block
        v2_signals_block = {
            "real_time_intel": signals_block,
            "composite_score": composite_score.get('composite_score', v1_profile.get('signals', {}).get('distress_level_score', 0)),
            "urgency_flag": composite_score.get('urgency_flag', 'MONITOR'),
            "v1_base_score": composite_score.get('v1_base_score'),
            "v2_contribution": composite_score.get('v2_amplification', 0),
            "signal_breakdown": composite_score.get('amplified_signals', [])
        }
        
        # Merge into profile
        enhanced_profile = v1_profile.copy()
        enhanced_profile['profile_version'] = '2.0.0'
        enhanced_profile['v2_signals'] = v2_signals_block
        
        # Update metadata
        if 'metadata' not in enhanced_profile:
            enhanced_profile['metadata'] = {}
        
        enhanced_profile['metadata']['analyst_version'] = '2.0.0-LITE'
        enhanced_profile['metadata']['intelligence_queries_used'] = raw_recon.get('queries_executed', 0)
        enhanced_profile['metadata']['schema_version'] = '2.0.0'
        
        return enhanced_profile
    
    def run_full_pipeline(
        self,
        v1_profile: Dict[str, Any],
        university_name: str,
        ein: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Execute complete V2.0-LITE pipeline (Phases 5-6).
        
        Args:
            v1_profile: Output from V1 analyst pipeline
            university_name: Full university name
            ein: Employer Identification Number
            
        Returns:
            Tuple of (enhanced_profile, metadata_dict)
        """
        
        metadata = {
            "v2_lite_enabled": self.enable_v2_lite,
            "phases_executed": [],
            "start_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        if not self.enable_v2_lite:
            metadata['phases_executed'] = ['V1 only']
            return v1_profile, metadata
        
        # Phase 5: Reconnaissance
        recon_results = self.run_v2_lite_recon(university_name, ein)
        metadata['phases_executed'].append('Phase 5 (Recon)')
        
        # Phase 5b: Signal Extraction
        extracted = self.run_signal_extraction(recon_results, university_name)
        metadata['phases_executed'].append('Phase 5b (Synthesis)')
        
        # Phase 6: Composite Scoring
        composite = self.run_composite_scoring(v1_profile, extracted.get('signals', self._get_null_signals()))
        metadata['phases_executed'].append('Phase 6 (Classification)')
        
        # Merge into profile
        enhanced_profile = self.merge_v2_into_profile(
            v1_profile=v1_profile,
            raw_recon=recon_results,
            extracted_signals=extracted,
            composite_score=composite
        )
        
        metadata['end_timestamp'] = datetime.now(timezone.utc).isoformat()
        metadata['status'] = 'complete'
        
        return enhanced_profile, metadata
    
    @staticmethod
    def _get_null_signals() -> Dict[str, Dict[str, str]]:
        """Return null signal structure for error handling."""
        return {
            "enrollment_trends": {
                "finding": "Unavailable",
                "source": "N/A",
                "credibility": "N/A"
            },
            "leadership_changes": {
                "finding": "Unavailable",
                "source": "N/A",
                "credibility": "N/A"
            },
            "accreditation_status": {
                "finding": "Unavailable",
                "source": "N/A",
                "credibility": "N/A"
            }
        }


def enhance_profile_with_v2_lite(
    v1_profile: Dict[str, Any],
    university_name: str,
    ein: str,
    enable_v2: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to enhance V1 profile with V2.0-LITE signals.
    
    Args:
        v1_profile: Original V1 analyst profile
        university_name: Full university name
        ein: Employer Identification Number
        enable_v2: Toggle V2-LITE features (default: enabled)
        
    Returns:
        Enhanced profile with v2_signals block (backward-compatible)
    """
    orchestrator = AnalystV2Orchestrator(enable_v2_lite=enable_v2)
    enhanced, _ = orchestrator.run_full_pipeline(v1_profile, university_name, ein)
    return enhanced
