#!/usr/bin/env python3
"""
Outreach Architect Agent for Charter & Stone
Converts Deep Dive Analyst intelligence into actionable cold outreach sequences.

Generates 3-stage email sequences (Cold Intro → Value Add → Break-up) 
tailored to institutional distress level using Claude 4.5 Sonnet via Anthropic API.
"""

import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import jsonschema
from anthropic import Anthropic

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agents/outreach/logs/outreach.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Forbidden phrases that indicate vendor-speak
FORBIDDEN_PHRASES = [
    "I wanted to reach out",
    "I wanted to share",
    "I wanted to follow up",
    "I wanted to connect",
    "I'd love to",
    "Circling back",
    "Just checking in",
    "Leveraging our platform",
    "Thought leadership",
    "Best-in-class solutions",
    "Your transformation journey",
    "synergy",
    "holistic",
    "leverage",
    "transformation",
    "let's schedule a demo",
    "I have solutions for you",
]

# Prospect profile schema (v1.0.0)
PROSPECT_SCHEMA = {
    "type": "object",
    "required": ["meta", "institution", "signals", "leadership"],
    "properties": {
        "meta": {
            "type": "object",
            "required": ["schema_version"],
            "properties": {
                "schema_version": {"type": "string", "pattern": "^1\\.0\\.0$"}
            }
        },
        "institution": {
            "type": "object",
            "required": ["name", "type"],
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string"},
                "location": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "state": {"type": "string"}
                    }
                }
            }
        },
        "financials": {
            "type": "object",
            "properties": {
                "calculated": {
                    "type": "object",
                    "properties": {
                        "expense_ratio": {"type": ["number", "null"]},
                        "runway_years": {"type": ["number", "null"]},
                        "tuition_dependency": {"type": ["number", "null"]}
                    }
                }
            }
        },
        "signals": {
            "type": "object",
            "required": ["distress_level"],
            "properties": {
                "distress_level": {
                    "type": "string",
                    "enum": ["critical", "elevated", "watch", "stable"]
                },
                "indicators": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "signal": {"type": "string"},
                            "severity": {"type": "string"}
                        }
                    }
                }
            }
        },
        "leadership": {
            "type": "object",
            "properties": {
                "key_contacts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "title": {"type": "string"}
                        }
                    }
                }
            }
        },
        "blinded_presentation": {
            "type": "object",
            "properties": {
                "display_name": {"type": "string"}
            }
        }
    }
}


class OutreachArchitect:
    """Main orchestrator for generating prospect outreach sequences."""

    def __init__(self):
        """Initialize the agent with Anthropic client and system prompt."""
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Please add it to .env and source it."
            )
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-opus-4-1-20250805"
        
        # Load system prompt
        prompt_path = Path(__file__).parent / "config" / "system_prompt.txt"
        with open(prompt_path, 'r') as f:
            self.system_prompt = f.read()

    def validate_profile(self, profile: Dict[str, Any]) -> bool:
        """
        Validate prospect profile against schema v1.0.0.
        
        Args:
            profile: Prospect profile dictionary
            
        Returns:
            True if valid
            
        Raises:
            jsonschema.ValidationError if schema invalid
            ValueError if schema version mismatch
        """
        try:
            jsonschema.validate(instance=profile, schema=PROSPECT_SCHEMA)
            logger.info("Profile schema validation passed")
            return True
        except jsonschema.ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            raise

    def check_forbidden_phrases(self, text: str) -> list:
        """
        Scan text for forbidden vendor-speak phrases.
        
        Args:
            text: Email body text to scan
            
        Returns:
            List of forbidden phrases found (empty if clean)
        """
        found = []
        text_lower = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in text_lower:
                found.append(phrase)
        return found

    def get_distress_triage(self, distress_level: str) -> Dict[str, Any]:
        """
        Determine tone and timing cadence based on distress level.
        
        Args:
            distress_level: One of "critical", "elevated", "watch", "stable"
            
        Returns:
            Dict with tone and timing parameters
            
        Raises:
            ValueError if distress_level is "stable" (abort outreach)
        """
        triage_map = {
            "critical": {
                "tone": "urgent_intervention",
                "timing_days": [0, 3, 7],
                "cadence_description": "Urgent cadence (0-3-7 days)"
            },
            "elevated": {
                "tone": "strategic_warning",
                "timing_days": [0, 5, 10],
                "cadence_description": "Strategic cadence (0-5-10 days)"
            },
            "watch": {
                "tone": "advisory_touch",
                "timing_days": [0, 7, 14],
                "cadence_description": "Advisory cadence (0-7-14 days)"
            },
            "stable": None
        }
        
        if distress_level == "stable":
            raise ValueError(
                "Stable institutions do not warrant cold outreach. Aborting."
            )
        
        return triage_map[distress_level]

    def build_generation_prompt(self, profile: Dict[str, Any], triage: Dict[str, Any]) -> str:
        """
        Build the user prompt for email generation based on profile data.
        
        Args:
            profile: Validated prospect profile
            triage: Distress triage information
            
        Returns:
            Formatted prompt for Claude
        """
        institution = profile["institution"]
        financials = profile.get("financials", {}).get("calculated", {})
        signals = profile.get("signals", {})
        leadership = profile.get("leadership", {}).get("key_contacts", [])
        
        # Build financial context
        expense_ratio = financials.get("expense_ratio")
        runway_years = financials.get("runway_years")
        tuition_dep = financials.get("tuition_dependency")
        
        # Format key contact
        contact_name = "CFO" if not leadership else f"{leadership[0].get('name', 'CFO')}, {leadership[0].get('title', '')}"
        
        # Build indicators summary
        indicators = signals.get("indicators", [])
        indicator_text = "\n".join([
            f"- {ind.get('signal', 'Unknown signal')} (severity: {ind.get('severity', 'medium')})"
            for ind in indicators[:3]  # Top 3 signals
        ])
        
        prompt = f"""Generate a 3-email cold outreach sequence for the following prospect:

**Institution:** {institution.get('name', 'Unknown')}
**Type:** {institution.get('type', 'Unknown')}
**Location:** {institution.get('location', {}).get('city', '')}, {institution.get('location', {}).get('state', '')}
**Distress Level:** {signals.get('distress_level', 'unknown').upper()}
**Tone Target:** {triage['tone']}
**Email Cadence:** {triage['cadence_description']}
**Primary Contact:** {contact_name}

**Financial Metrics:**
- Expense Ratio: {expense_ratio if expense_ratio else 'N/A'}
- Runway (Years): {runway_years if runway_years else 'N/A'}
- Tuition Dependency: {tuition_dep}%

**Distress Signals:**
{indicator_text}

**Instructions:**
1. Generate 3 emails following the strict rules in your system prompt
2. Email 1 (Cold Intro): Hook on a specific signal, offer diagnostic value, ask for 20-min conversation
3. Email 2 (Value Add): Share 1-2 financial insights, reiterate it's a diagnostic conversation, NOT a pitch
4. Email 3 (Break-up): Acknowledge non-response, leave door open, NO guilt trips
5. Use plain business English—NO jargon, NO vendor-speak
6. Treat the recipient as an equal peer-to-peer
7. Return valid JSON with email_1, email_2, email_3 objects (each with subject and body)

Generate the emails now."""
        
        return prompt

    def generate_emails(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call Anthropic API to generate email sequence.
        
        Args:
            profile: Validated prospect profile
            
        Returns:
            Dict with email_1, email_2, email_3, and analysis
            
        Raises:
            Various errors from Anthropic API or JSON parsing
        """
        logger.info(f"Generating outreach for {profile['institution']['name']}")
        
        # Triage by distress level
        distress = profile["signals"]["distress_level"]
        triage = self.get_distress_triage(distress)
        
        # Build generation prompt
        user_prompt = self.build_generation_prompt(profile, triage)
        
        # Call Claude
        logger.info(f"Calling Anthropic API (model: {self.model})")
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Parse response
        response_text = message.content[0].text
        logger.info("API call successful")
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                emails = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from API response: {e}")
            logger.error(f"Response: {response_text}")
            raise
        
        return emails

    def validate_email_content(self, emails: Dict[str, Any]) -> list:
        """
        Check generated emails for forbidden phrases.
        
        Args:
            emails: Dict with email_1, email_2, email_3
            
        Returns:
            List of violations found
        """
        violations = []
        
        for email_key in ["email_1", "email_2", "email_3"]:
            if email_key not in emails:
                continue
            
            email = emails[email_key]
            subject = email.get("subject", "")
            body = email.get("body", "")
            
            subject_violations = self.check_forbidden_phrases(subject)
            body_violations = self.check_forbidden_phrases(body)
            
            all_violations = subject_violations + body_violations
            if all_violations:
                violations.append({
                    "email": email_key,
                    "phrases_found": list(set(all_violations))
                })
        
        if violations:
            logger.warning(f"Found {len(violations)} emails with forbidden phrases")
            for v in violations:
                logger.warning(f"{v['email']}: {v['phrases_found']}")
        else:
            logger.info("All emails passed forbidden phrase check")
        
        return violations

    def generate_markdown_output(
        self, 
        profile: Dict[str, Any], 
        emails: Dict[str, Any],
        violations: list
    ) -> str:
        """
        Assemble emails into Markdown output file.
        
        Args:
            profile: Prospect profile
            emails: Generated emails dict
            violations: List of forbidden phrase violations
            
        Returns:
            Markdown string
        """
        institution_name = profile["institution"]["name"]
        distress_level = profile["signals"]["distress_level"]
        leadership = profile.get("leadership", {}).get("key_contacts", [])
        contact = leadership[0] if leadership else {"name": "CFO", "title": ""}
        
        timestamp = datetime.now().isoformat()
        
        md = f"""# Outreach Sequence: {institution_name}

**Generated:** {timestamp}  
**Distress Level:** {distress_level.upper()}  
**Target Contact:** {contact.get('name', 'CFO')}, {contact.get('title', '')}

---

## Email 1: Cold Intro
**Subject:** {emails.get('email_1', {}).get('subject', 'N/A')}  
**Timing:** Day 0

{emails.get('email_1', {}).get('body', 'N/A')}

---

## Email 2: Value Add
**Subject:** {emails.get('email_2', {}).get('subject', 'N/A')}  
**Timing:** Day 5-7 (if no response)

{emails.get('email_2', {}).get('body', 'N/A')}

---

## Email 3: Break-up
**Subject:** {emails.get('email_3', {}).get('subject', 'N/A')}  
**Timing:** Day 10-14 (if no response)

{emails.get('email_3', {}).get('body', 'N/A')}

---

## Analyst Notes
{emails.get('analysis', 'No additional notes')}

---

## Quality Control
"""
        
        if violations:
            md += f"⚠️ **WARNING:** Found forbidden phrases in {len(violations)} email(s):\n"
            for v in violations:
                md += f"- {v['email']}: {', '.join(v['phrases_found'])}\n"
            md += "\n**Action Required:** Human review recommended before sending.\n"
        else:
            md += "✓ All emails passed forbidden phrase validation.\n"
        
        md += f"\n**Financial Context:**\n"
        financials = profile.get("financials", {}).get("calculated", {})
        md += f"- Expense Ratio: {financials.get('expense_ratio', 'N/A')}\n"
        md += f"- Runway (Years): {financials.get('runway_years', 'N/A')}\n"
        md += f"- Tuition Dependency: {financials.get('tuition_dependency', 'N/A')}%\n"
        
        return md

    def process_prospect(self, profile_path: str) -> Dict[str, Any]:
        """
        Main orchestrator: Load, validate, generate, and save outreach.
        
        Args:
            profile_path: Path to prospect_profile.json
            
        Returns:
            Result dict with file path and metadata
        """
        try:
            # Step 1: Load profile
            logger.info(f"Loading profile: {profile_path}")
            with open(profile_path, 'r') as f:
                profile = json.load(f)
            
            # Step 2: Validate schema
            self.validate_profile(profile)
            
            # Step 3: Check distress level (abort if stable)
            distress = profile["signals"]["distress_level"]
            if distress == "stable":
                logger.warning("Institution is stable. Aborting outreach generation.")
                return {
                    "status": "aborted",
                    "reason": "Stable institution",
                    "institution": profile["institution"]["name"]
                }
            
            # Step 4: Generate emails
            emails = self.generate_emails(profile)
            
            # Step 5: Validate content
            violations = self.validate_email_content(emails)
            
            # Step 6: Assemble Markdown
            markdown = self.generate_markdown_output(profile, emails, violations)
            
            # Step 7: Save output
            institution_name = profile["institution"]["name"].replace(" ", "_").lower()
            output_path = Path("agents/outreach/outputs") / f"{institution_name}_outreach_sequence.md"
            
            with open(output_path, 'w') as f:
                f.write(markdown)
            
            logger.info(f"Outreach sequence saved to {output_path}")
            
            return {
                "status": "success",
                "file_path": str(output_path),
                "institution": profile["institution"]["name"],
                "distress_level": distress,
                "emails_generated": 3,
                "violations": violations
            }
        
        except Exception as e:
            logger.error(f"Error processing prospect: {str(e)}", exc_info=True)
            raise


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python outreach.py <path_to_profile.json>")
        print("Example: python outreach.py knowledge_base/prospects/albright_college_profile.json")
        sys.exit(1)
    
    profile_path = sys.argv[1]
    
    if not os.path.exists(profile_path):
        print(f"Error: Profile file not found: {profile_path}")
        sys.exit(1)
    
    try:
        architect = OutreachArchitect()
        result = architect.process_prospect(profile_path)
        
        print("\n" + "="*60)
        print("OUTREACH ARCHITECT EXECUTION SUMMARY")
        print("="*60)
        for key, value in result.items():
            print(f"{key.upper()}: {value}")
        print("="*60)
        
        if result["status"] == "success":
            print(f"\n✓ Outreach sequence generated successfully")
            print(f"📄 Output: {result['file_path']}")
            if result["violations"]:
                print(f"\n⚠️  WARNING: {len(result['violations'])} email(s) contain forbidden phrases")
                print("   Please review before sending")
            sys.exit(0)
        else:
            print(f"\n⊘ Generation skipped: {result['reason']}")
            sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
