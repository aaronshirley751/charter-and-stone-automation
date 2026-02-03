"""
Charter & Stone Analyst V2.0-LITE Intelligence Layer
Real-time intelligence augmentation for IRS 990 data via Perplexity Sonar API.

Modules:
  - recon: 3-query Perplexity orchestrator
  - synthesis: Claude-powered signal extraction with citation discipline
  - classification: Composite V1+V2 scoring logic

Version: 2.0.0-LITE
Authorization: OPERATION_SNIPER_FINAL_AUTHORIZATION_V2_LITE.md
"""

from .recon import execute_recon
from .synthesis import extract_signals
from .classification import calculate_composite_score

__all__ = [
    'execute_recon',
    'extract_signals',
    'calculate_composite_score',
]

__version__ = '2.0.0-LITE'
