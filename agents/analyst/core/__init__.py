"""
Charter & Stone Analyst Core Modules

Orchestration and pipeline management for Analyst V2.0-LITE.
"""

from .orchestrator import (
    AnalystV2Orchestrator,
    enhance_profile_with_v2_lite
)

__version__ = "2.0.0-LITE"

__all__ = [
    'AnalystV2Orchestrator',
    'enhance_profile_with_v2_lite',
    '__version__',
]
