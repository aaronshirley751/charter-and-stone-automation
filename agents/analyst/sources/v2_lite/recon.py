"""
RECON MODULE: Perplexity Sonar 3-Query Orchestrator
Executes structured web reconnaissance for university distress signals.

License Constraint: 3-query budget per university per run.
Authorization: OPERATION_SNIPER_FINAL_AUTHORIZATION_V2_LITE.md
"""

import json
import requests
import time
from typing import Dict, Optional, Any
from datetime import datetime, timezone
import os


class PerplexityReconClient:
    """
    Orchestrates 3 Perplexity Sonar queries optimized for distressed university detection.
    
    Query Budget:
      1. Enrollment & Financial Stress
      2. Leadership Changes
      3. Accreditation & Regulatory
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Perplexity client with API key."""
        self.api_key = api_key or os.environ.get('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment or constructor")
        
        self.base_url = "https://api.perplexity.ai"
        self.model = "sonar"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Charter-Stone-Analyst-V2/2.0'
        })
        self.query_count = 0
        self.query_budget = 3
    
    def _call_perplexity(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Execute single Perplexity Sonar search.
        
        Args:
            query: Search query string
            max_results: Maximum results to return
            
        Returns:
            Dictionary with results or error information
        """
        if self.query_count >= self.query_budget:
            raise RuntimeError(f"Query budget exhausted ({self.query_count}/{self.query_budget})")
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            self.query_count += 1
            result = response.json()
            
            return {
                "status": "success",
                "query": query,
                "response": result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "query": query,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def execute_recon(self, university_name: str, ein: str) -> Dict[str, Any]:
        """
        Execute 3-query reconnaissance for university.
        
        Query 1: Enrollment & Financial Stress
        Query 2: Leadership Changes  
        Query 3: Accreditation & Regulatory
        
        Args:
            university_name: Full university name
            ein: Employer Identification Number
            
        Returns:
            Dictionary with raw search results and metadata
        """
        
        self.query_count = 0
        results = {
            "enrollment_financial": None,
            "leadership": None,
            "accreditation": None
        }
        
        # Query 1: Enrollment & Financial Stress
        query_1 = (
            f'"{university_name}" enrollment decline financial crisis '
            f'operating deficit 2024 2025'
        )
        results['enrollment_financial'] = self._call_perplexity(query_1)
        time.sleep(0.5)  # Rate limiting
        
        # Query 2: Leadership Changes
        query_2 = (
            f'"{university_name}" president CFO resignation interim appointment '
            f'leadership change 2024 2025'
        )
        results['leadership'] = self._call_perplexity(query_2)
        time.sleep(0.5)
        
        # Query 3: Accreditation & Regulatory
        query_3 = (
            f'"{university_name}" accreditation probation MSCHE HLC '
            f'closure warning regulatory 2024 2025'
        )
        results['accreditation'] = self._call_perplexity(query_3)
        
        return {
            "raw_results": results,
            "queries_executed": self.query_count,
            "queries_budget": self.query_budget,
            "university_name": university_name,
            "ein": ein,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def execute_recon(university_name: str, ein: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for executing reconnaissance.
    
    Args:
        university_name: Full university name
        ein: Employer Identification Number
        api_key: Optional API key (uses env variable if not provided)
        
    Returns:
        Raw reconnaissance results from 3 Perplexity queries
    """
    client = PerplexityReconClient(api_key=api_key)
    return client.execute_recon(university_name, ein)
