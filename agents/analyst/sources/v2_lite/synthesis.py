"""
SYNTHESIS MODULE: Claude-Powered Intelligence Signal Extraction
Extracts structured, actionable signals from Perplexity search results.

Core Principles:
  - Anti-Vendor Philosophy: We sell judgment, not data dumps
  - Blinded Diagnostics: External data sources only
  - Citation Discipline: Every finding must cite source with date
  - Binary Credibility: TRUSTED or UNTRUSTED (no weighted scores)

Authorization: OPERATION_SNIPER_FINAL_AUTHORIZATION_V2_LITE.md
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timezone


class SynthesisEngine:
    """
    Claude-powered signal extraction from raw Perplexity results.
    Enforces citation discipline and binary credibility classification.
    """
    
    def __init__(self, api_key: Optional[str] = None, system_prompt_path: Optional[str] = None):
        """Initialize Claude client and load system prompt."""
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or constructor")
        
        try:
            import anthropic
        except ImportError as exc:
            raise ImportError(
                "anthropic package is required for V2-LITE synthesis."
            ) from exc
        
        self.client = anthropic.Anthropic(api_key=self.api_key, timeout=90.0)
        self.model = "claude-3-sonnet-20240229"  # Standard Sonnet model (broader compatibility)
        
        # Load system prompt
        if system_prompt_path:
            with open(system_prompt_path, 'r') as f:
                self.system_prompt = f.read()
        else:
            self.system_prompt = self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Return default system prompt if not loaded from file."""
        return """# SYSTEM PROMPT: INTELLIGENCE SYNTHESIS ENGINE (V2.0-LITE)

## MISSION
You are the Intelligence Synthesis module for Charter & Stone's Analyst Agent V2.0-LITE.
Your role: Extract structured, actionable signals from web search results about distressed universities.

## CORE PRINCIPLES
1. **Anti-Vendor Philosophy**: We sell judgment, not data dumps. Every finding must be decision-ready.
2. **Blinded Diagnostics**: We only use external, public data sources. No insider info.
3. **Citation Discipline**: Every claim requires source attribution with publication date.

## OUTPUT REQUIREMENTS

### STRUCTURE
You MUST return valid JSON with exactly three signal categories:
- `enrollment_trends`: Evidence of student recruitment/retention problems
- `leadership_changes`: C-suite turnover, interim appointments, resignations
- `accreditation_status`: Regulatory warnings, probation, compliance issues

### CREDIBILITY CLASSIFICATION (BINARY ONLY)
- **TRUSTED**: .edu domains, .gov sites, Chronicle/Inside Higher Ed, WSJ, NYT, Bloomberg, official accreditor disclosures
- **UNTRUSTED**: Forums, blogs, Reddit, unverified social media, press releases without third-party confirmation

**CRITICAL**: Do NOT use weighted scores (e.g., "85% credible"). Classification is BINARY: TRUSTED or UNTRUSTED.

### CITATION FORMAT
Every finding MUST include:
- `source`: "Publication Name, YYYY-MM-DD"
- Example: "Chronicle of Higher Education, 2024-11-15"

### INSUFFICIENT EVIDENCE HANDLING
If search results contain no credible signals for a category, return:
```json
{
  "finding": "No credible signals detected",
  "source": "Search corpus reviewed 2025-02-03",
  "credibility": "N/A"
}
```

## WHAT TO IGNORE
- Marketing fluff (e.g., "X University announces exciting new program")
- Opinion pieces without factual claims
- Paywalled content where snippet doesn't contain actionable data
- Duplicate reports of the same event

## TONE
- Factual, clinical, no editorializing
- "Enrollment declined 12%" not "Enrollment suffered a devastating blow"
- Let the numbers speak

## FAILURE MODES TO AVOID
- Citing forums or Reddit as credible sources
- Omitting publication dates
- Using confidence percentages or weighted scores
- Editorializing findings with subjective language
- Returning malformed JSON
"""
    
    def extract_signals(self, raw_perplexity_results: Dict[str, Any], university_name: str) -> Dict[str, Any]:
        """
        Extract structured signals from raw Perplexity results using Claude.
        
        Args:
            raw_perplexity_results: Dictionary with enrollment_financial, leadership, accreditation results
            university_name: Name of university being analyzed
            
        Returns:
            Dictionary with extracted signals (enrollment_trends, leadership_changes, accreditation_status)
        """
        
        # Construct Claude prompt
        user_prompt = f"""MISSION: Extract actionable intelligence signals for {university_name}.

RAW SEARCH RESULTS:
{json.dumps(raw_perplexity_results, indent=2)}

OUTPUT FORMAT: You MUST return ONLY valid JSON (no markdown, no code blocks, just JSON) with structure:
{{
  "enrollment_trends": {{
    "finding": "specific factual claim",
    "source": "publication name, date",
    "credibility": "TRUSTED|UNTRUSTED|N/A"
  }},
  "leadership_changes": {{
    "finding": "specific factual claim",
    "source": "publication name, date",
    "credibility": "TRUSTED|UNTRUSTED|N/A"
  }},
  "accreditation_status": {{
    "finding": "specific factual claim",
    "source": "publication name, date",
    "credibility": "TRUSTED|UNTRUSTED|N/A"
  }}
}}

GUARDRAILS:
- Every finding MUST cite source with date.
- Credibility is BINARY: TRUSTED (original sources, .edu, .gov, major pubs) or UNTRUSTED (forums, blogs, unverified).
- If insufficient evidence, return finding: "No credible signals detected".
- NO weighted scores. NO confidence percentages.
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=0.3  # Low temperature for factual extraction
            )
            
            # Extract response text
            response_text = response.content[0].text
            
            # Parse JSON response
            try:
                structured_signals = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0].strip()
                    structured_signals = json.loads(json_str)
                elif "```" in response_text:
                    json_str = response_text.split("```")[1].split("```")[0].strip()
                    structured_signals = json.loads(json_str)
                else:
                    raise
            
            # Add metadata
            return {
                "signals": structured_signals,
                "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
                "university_name": university_name,
                "model": self.model,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "signals": {
                    "enrollment_trends": {
                        "finding": "Extraction failed",
                        "source": "Error occurred during processing",
                        "credibility": "N/A"
                    },
                    "leadership_changes": {
                        "finding": "Extraction failed",
                        "source": "Error occurred during processing",
                        "credibility": "N/A"
                    },
                    "accreditation_status": {
                        "finding": "Extraction failed",
                        "source": "Error occurred during processing",
                        "credibility": "N/A"
                    }
                },
                "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
                "university_name": university_name,
                "model": self.model,
                "status": "error",
                "error": str(e)
            }


def extract_signals(
    raw_perplexity_results: Dict[str, Any],
    university_name: str,
    api_key: Optional[str] = None,
    system_prompt_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function for signal extraction.
    
    Args:
        raw_perplexity_results: Dictionary with search results from recon module
        university_name: Name of university
        api_key: Optional Claude API key
        system_prompt_path: Optional path to custom system prompt
        
    Returns:
        Dictionary with extracted signals
    """
    engine = SynthesisEngine(api_key=api_key, system_prompt_path=system_prompt_path)
    return engine.extract_signals(raw_perplexity_results, university_name)
