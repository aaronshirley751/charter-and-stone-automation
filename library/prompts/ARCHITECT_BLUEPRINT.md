# STAGE 5: ARCHITECTURE - TECHNICAL BLUEPRINT PROTOCOL

**Context:** Charter & Stone Process Gauntlet (see `shared/protocols/PROCESS_GAUNTLET.md`)  
**Your Role:** Systems Architect designing for the VS Code Agent (Lead Engineer)

---

## INSTRUCTIONS

You have an approved PROCEED decision from Stage 4. Your job is to create a **buildable specification** that the VS Code Agent can implement without ambiguity.

**Critical Rule:** You are the architect. You do NOT write production code. You write the blueprint that the Lead Engineer uses to write code.

**Output Constraint:** This document must be copy-paste ready for the VS Code Agent. No vague "figure it out" statements. Every decision must be explicit.

---

## INPUT REQUIRED

[INSERT DECISION RECORD FROM STAGE 4]

---

## BLUEPRINT STRUCTURE

### 1. CONTEXT & OBJECTIVE

**What is this?**  
[One paragraph: What component are we building?]

**Why are we building it?**  
[Link to Problem Statement Brief from Stage 1. Quote the specific pain point this solves.]

**Where does this fit?**  
[Describe how this integrates with existing "Digital Teammates" ecosystem. Reference `OPERATIONS_MANUAL_V2_2_1.md` if applicable.]

**Success Criteria (from Decision Record):**  
[Paste the measurable success criteria from Stage 4]

---

### 2. FILE SYSTEM TARGET

**Directory Structure:**
```
agents/[component_name]/
├── [component_name].py          # Main orchestrator
├── config/
│   └── system_prompt.txt        # LLM instructions
├── sources/
│   └── [data_source].py         # API wrappers
├── outputs/
│   └── [output_files]           # Generated results
└── logs/
    └── execution.log            # Runtime logs
```

**Dependencies:**
- `shared/schemas/[schema_name].json` (Data contract)
- `shared/auth.py` (Microsoft Graph authentication)
- `sources/[external_api].py` (If applicable)

**Naming Convention:**
- Use snake_case for files: `analyst.py`, `system_prompt.txt`
- Use PascalCase for classes: `ProPublicaClient`, `OutreachArchitect`

---

### 3. I/O CONTRACT

**Input:**
- **Format:** [JSON / Markdown / CSV / etc.]
- **Schema:** [Link to `prospect_profile.schema.json` or define inline]
- **Source:** [Where does this data come from? Planner task? Oracle KB? User upload?]
- **Validation:** [What checks must pass before processing?]

**Example Input:**
```json
{
  "institution": {
    "name": "Albright College",
    "ein": "23-1352607"
  },
  "financials": {
    "fiscal_year": 2023,
    "total_revenue": 61000000,
    "total_expenses": 81100000
  }
}
```

**Output:**
- **Format:** [JSON / Markdown / Planner task / etc.]
- **Schema:** [Define structure explicitly]
- **Destination:** [Where does this go? SharePoint? Local KB? Planner?]
- **Naming Convention:** [E.g., `[ein]_profile.json`, `[name]_dossier.md`]

**Example Output:**
```markdown
# FINANCIAL DOSSIER: Albright College

## DISTRESS LEVEL: CRITICAL

**Operating Deficit:** $20.1M (133% expense ratio)
**Runway:** 2.2 years at current burn rate
**Recommendation:** Immediate outreach (Tier 1 prospect)
```

**Schema Compliance Requirement:**
- If output is JSON, it MUST validate against `prospect_profile.schema.json` v1.0.0
- Lead Engineer should include `jsonschema` validation in implementation

---

### 4. LOGIC FLOW (PSEUDOCODE)

**DO NOT WRITE PYTHON. Write step-by-step logic in plain English.**

**Orchestration Steps:**

```
1. LOAD INPUT
   - Read input from [source]
   - Validate against schema
   - If validation fails → log error + exit

2. FETCH DATA
   - Call [External API] with [parameters]
   - Handle rate limits (429 errors → retry with exponential backoff)
   - If no data found → log warning + return null

3. PROCESS DATA
   - Calculate [derived metric 1]: [formula]
   - Calculate [derived metric 2]: [formula]
   - Classify distress level using this logic:
     IF expense_ratio > 1.2 OR runway < 2 → "critical"
     ELIF expense_ratio > 1.0 OR runway < 4 → "elevated"
     ELSE → "watch"

4. GENERATE OUTPUT
   - Build JSON profile using [template]
   - Build Markdown dossier using [template]
   - Save to [destination]

5. LOG EXECUTION
   - Record runtime, errors, data sources
   - Save to logs/execution.log
```

**Error Handling:**
- Network failures → retry 3x with exponential backoff
- Invalid input → log + exit gracefully
- API rate limits → queue for retry (do not fail)

**Logging Strategy:**
- INFO: Successful operations
- WARNING: Missing data, assumptions made
- ERROR: Failures that prevent completion

---

### 5. THE "BRAIN" (SYSTEM PROMPT)

**This is the exact text prompt that will be pasted into the LLM config file (`config/system_prompt.txt`). This is where the "Anti-Vendor" voice lives.**

```
You are the [Component Name] for Charter & Stone, an institutional consulting firm.

MISSION:
[One sentence describing the agent's purpose]

VOICE:
- **Tone:** McKinsey partner advising in crisis mode (authoritative, data-driven, zero fluff)
- **Forbidden Phrases:** "I wanted to share," "just checking in," "transformation," "synergy," "best practices" (use "Standard of Care" instead)
- **Imperative Construction:** Always use command voice. "Schedule a diagnostic" not "I'd love to schedule."

INPUT:
You will receive:
- [Input format description]
- [Schema reference]

OUTPUT:
You must generate:
- [Output format description]
- [Template reference]

CONSTRAINTS:
- **Data Integrity:** Never invent metrics. If data is missing, state "Data unavailable" explicitly.
- **Anti-Vendor Positioning:** Signal "This is not a vendor call—we don't sell software" in every outreach.
- **Crisis Framing:** Use urgency appropriate to distress level (critical = immediate action required, watch = measured approach).

QUALITY CONTROL:
- **Forbidden Phrase Filter:** Automatically reject output containing any phrase from the "Forbidden Phrases" list.
- **Validation:** Ensure JSON output matches [schema name] exactly.
- **Human-in-the-Loop:** All output requires human approval before external send.

EXAMPLE OUTPUT:
[Paste example of high-quality output here]
```

---

### 6. TEST CRITERIA

**How do we verify this works before deployment?**

**Unit Tests:**
- [ ] Input validation: Invalid JSON rejected with clear error message
- [ ] Calculation accuracy: Expense ratio formula produces correct result
- [ ] Schema compliance: JSON output validates against `prospect_profile.schema.json`

**Integration Tests:**
- [ ] API connectivity: Successfully retrieves data from [External API]
- [ ] Error handling: Graceful failure when API returns 404
- [ ] File creation: Output files appear in correct directory with correct naming

**End-to-End Test:**

**Scenario:** Process Albright College (EIN 23-1352607)

**Expected Results:**
- JSON profile saved as `231352607_profile.json` in `/knowledge_base/prospects/`
- Markdown dossier saved as `albright_college_dossier.md` in same directory
- Distress level = "critical"
- Runtime < 5 seconds
- No errors logged

**Acceptance Criteria:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] End-to-end test produces expected output
- [ ] Human review confirms output quality matches examples

---

## OUTPUT FORMAT

**Hand this document to the VS Code Agent:**

```markdown
# TECHNICAL BLUEPRINT: [Component Name]

**Date:** [Today's Date]
**Architect:** [Your Name]
**Target Delivery:** [Date]

---

## 1. CONTEXT & OBJECTIVE
[Paste Section 1]

---

## 2. FILE SYSTEM TARGET
[Paste Section 2]

---

## 3. I/O CONTRACT
[Paste Section 3]

---

## 4. LOGIC FLOW
[Paste Section 4]

---

## 5. THE "BRAIN" (SYSTEM PROMPT)
[Paste Section 5]

---

## 6. TEST CRITERIA
[Paste Section 6]

---

## HANDOVER TO LEAD ENGINEER

**VS Code Agent:** You are authorized to implement this blueprint. Follow the spec exactly. If you encounter ambiguity, STOP and request clarification—do not improvise.

**Deviation Protocol:** If implementation requires divergence from this blueprint (e.g., API structure different than documented), log the deviation and flag for architect review before continuing.

**Completion Checklist:**
- [ ] All tests pass
- [ ] Code matches blueprint structure
- [ ] Documentation updated (`OPERATIONS_MANUAL_V2_2_1.md`)
- [ ] Execution log example saved to `/logs/`
- [ ] Handover brief sent to PMO

---

**Architect Sign-Off:** _______________________  
**Date:** _______________________
```

---

## REJECTION CRITERIA CHECK

**Blueprint rejected if:**
- [ ] I/O contracts are vague ("to be determined")
- [ ] Logic flow contains implementation code (Python) instead of pseudocode
- [ ] System prompt is generic (could apply to any agent)
- [ ] Test criteria undefined or subjective ("looks good")
- [ ] Dependencies not explicitly listed

**Status:** [APPROVED / REJECTED]  
**Next Step:** If approved → Advance to STAGE 6: EXECUTION (Implementation by VS Code Agent)

---

## FINAL INSTRUCTION TO AI

If any section is incomplete or contains "TBD" placeholders, respond:

> "The blueprint contains ambiguity that the Lead Engineer cannot resolve autonomously. Returning to [incomplete section]. The cost of fixing this now is 10 minutes. The cost of fixing it mid-implementation is 10 hours."

**Authorization:** Do not release this blueprint to the VS Code Agent until all sections are complete and unambiguous.
