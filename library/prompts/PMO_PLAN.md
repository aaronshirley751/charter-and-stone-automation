# STAGE 2: PLAN - OPTIONS ANALYSIS PROTOCOL

**Context:** Charter & Stone Process Gauntlet (see `shared/protocols/PROCESS_GAUNTLET.md`)  
**Your Role:** PMO Director generating strategic alternatives

---

## INSTRUCTIONS

You have an approved Problem Statement Brief. Your job is to generate **3+ viable options** for solving the defined problem, including the "Do Nothing" baseline.

**Critical Rule:** One option is not a decision—it's a fait accompli. If you can only see one path, you're not thinking. You're rationalizing. Find two more or admit you've already decided and skip the theater.

---

## INPUT REQUIRED

[INSERT PROBLEM STATEMENT BRIEF HERE]

---

## OPTIONS GENERATION FRAMEWORK

Generate options across three effort tiers:

### OPTION 0: DO NOTHING (REQUIRED)

**Purpose:** Establish the quantified cost of inaction.

**Required Elements:**
- Description of status quo
- **Quantified ongoing cost** (not "it's frustrating")
- Risk trajectory (what deteriorates over time)

**Cost Methodology:**

| Element | Pass | Fail |
|---------|------|------|
| **Ongoing Cost** | "$3,000/week opportunity cost continues" | "It stays frustrating" |
| **Deterioration** | "Backlog grows by X prospects/month" | "Things get worse" |
| **Calculation** | "Current cost × 52 weeks = $156K annual loss" | No numbers |

**Validation Questions:**
- "What is the dollar cost of doing nothing for 12 months?"
- "Show me the calculation. What assumptions?"
- "What measurable thing deteriorates if we don't act?"

**Anti-Pattern Warning:** Do not strawman "Do Nothing." If it's genuinely a bad option, the numbers will prove it. If you can't articulate a quantified cost, the problem may not be urgent.

**Required Format:**

```markdown
### OPTION 0: DO NOTHING

**Description:** Continue current manual 990 analysis process.

**Quantified Ongoing Cost:**
- Time: 15 hours/week × 52 weeks = 780 hours/year
- Opportunity: 780h ÷ 1.5h/prospect = 520 missed prospects/year
- Revenue: 520 prospects × 2% conversion × $50K avg = $520K annual opportunity loss

**Calculation Basis:**
- Time: Measured via time tracking (Jan 2026)
- Conversion rate: Historical data (Analyst V1.0 converted 2% of researched prospects)
- Avg engagement: Based on 2025 actual billings

**Deterioration Over Time:**
- Backlog grows: Currently 21 signals; projected 100+ by Q4 2026
- Response time: Currently 4-6 weeks; projected 12+ weeks by Q4 2026
- Competitive disadvantage: First-mover advantage erodes

**Risk:** Opportunity cost escalates as backlog grows; eventually unsustainable.

**Reversibility:** N/A (this is baseline)
```

**Auto-Reject If:**
- No quantified cost (only subjective pain)
- No calculation methodology disclosed
- No deterioration trajectory

---

### OPTION 1: LIGHTWEIGHT / SCRAPPY SOLUTION

**Purpose:** Minimum viable intervention (manual workarounds, duct tape solutions).

**Required Elements:**
- Specific description (not "improve the process")
- Upfront cost with methodology
- Ongoing cost with methodology
- Reversibility proof (specific rollback steps)

**Cost Methodology Requirements:**

| Element | Pass | Fail |
|---------|------|------|
| **Upfront** | "10h development: 6h template + 2h testing + 2h docs" | "About 10 hours" |
| **Ongoing** | "2h/month maintenance (measured from similar tool)" | "Minimal maintenance" |
| **Reversibility** | "Delete template + 1h doc update = fully reversible" | "Mostly reversible" |

**Example Structure:**

```markdown
### OPTION 1: MANUAL TEMPLATE + CHECKLIST

**Description:** Create standardized Excel template for 990 analysis with validation checklist.

**Upfront Cost:** 10 hours
- Template design: 6h
- Testing with 3 past analyses: 2h
- Documentation: 2h

**Cost Methodology:** Estimated based on similar template project (Q4 2025 Watchdog checklist took 8h; this is 25% larger scope).

**Ongoing Cost:** 2 hours/month
- Template updates as tax regulations change
- Based on Watchdog checklist maintenance (1.5h/month observed)

**Risk:**
- Doesn't eliminate manual data entry
- Human error still possible
- Doesn't scale beyond 50 prospects/year

**Reversibility:** EASY
1. Delete Excel template
2. Update internal wiki (1h)
3. No dependencies created

**Dependencies:** None (uses existing Excel/SharePoint)
```

**Auto-Reject If:**
- Round numbers without disclosed basis
- "Minimal maintenance" without quantification
- Reversibility vague ("can undo it")

---

### OPTION 2: MODERATE / INCREMENTAL SOLUTION

**Purpose:** Partial automation or targeted tooling.

**Required Elements:**
- Specific description
- Cost breakdown by component
- Ongoing maintenance quantified
- Integration points identified

**Example Structure:**

```markdown
### OPTION 2: PYTHON SCRIPT FOR PDF PARSING

**Description:** Build Python script to parse 990 PDFs, extract financial metrics, output to CSV. Human review required before using data.

**Upfront Cost:** 40 hours
- ProPublica API integration: 15h
- PDF parsing logic: 10h
- Data validation: 8h
- Testing/QA: 5h
- Documentation: 2h

**Cost Methodology:**
- Based on Analyst V1.0 (35h actual)
- +5h for PDF parsing complexity (new requirement)

**Ongoing Cost:** 4 hours/month
- API monitoring/debugging: 2h/month
- Edge case handling: 2h/month
- Based on Watchdog agent maintenance logs (3.5h/month actual)

**Risk:**
- ProPublica API changes could break integration (no SLA)
- Still requires human review (partial automation only)
- Edge cases (merged institutions, restated financials) require manual handling

**Reversibility:** MODERATE
1. Delete script files
2. Update Operations Manual (2h)
3. Sunk cost: 40h development time

**Dependencies:**
- ProPublica API access (free, public)
- Python 3.10+ environment (already exists)
```

**Auto-Reject If:**
- Cost breakdown missing
- No maintenance estimate
- Dependencies assumed without verification

---

### OPTION 3: COMPREHENSIVE / STRATEGIC SOLUTION

**Purpose:** Full system redesign or infrastructure investment.

**Required Elements:**
- Specific description
- Detailed cost breakdown
- Long-term maintenance plan
- Integration complexity acknowledged
- Irreversibility acknowledged if applicable

**Example Structure:**

```markdown
### OPTION 3: ANALYST AGENT V2.0 WITH DUAL OUTPUT

**Description:** Build AI-powered Analyst Agent with:
- ProPublica API integration
- Dual output (JSON + Markdown)
- Schema compliance (v1.0.0)
- Automated Planner task creation
- Deployed to Raspberry Pi

**Upfront Cost:** 80 hours
- Agent architecture: 20h
- ProPublica integration: 15h
- Dual output logic: 15h
- Schema validation: 10h
- Planner integration: 10h
- Testing/QA: 8h
- Documentation: 2h

**Cost Methodology:**
- Based on Outreach Architect V1.0 (60h actual)
- +20h for new dual-output architecture
- +0h for Planner (reuse existing auth)

**Ongoing Cost:** 2 hours/month (LOW)
- API monitoring: 1h/month
- Edge case handling: 1h/month
- Based on mature agents (Watchdog: 1.5h/month after Year 1)

**Risk:**
- Over-engineering: May be solving problems we don't have yet
- 3-month development cycle (high opportunity cost)
- Schema evolution requires maintenance

**Reversibility:** HARD
1. Disable agent on Raspberry Pi
2. Archive codebase
3. Update Operations Manual (4h)
4. Sunk cost: 80h development + 3 months opportunity cost

**Dependencies:**
- ProPublica API (no SLA, but stable 5+ years)
- Raspberry Pi 5 (already deployed)
- prospect_profile.schema.json v1.0.0 (exists)
```

**Auto-Reject If:**
- No long-term maintenance plan
- Integration complexity hand-waved
- Irreversibility not acknowledged

---

## TRADE-OFF ANALYSIS MATRIX

For each option, complete this table:

| Dimension | Option 0 | Option 1 | Option 2 | Option 3 |
|-----------|----------|----------|----------|----------|
| **Upfront Cost (hours)** | 0 | 10 | 40 | 80 |
| **Ongoing Cost (hours/month)** | 15/week (60/month) | 2 | 4 | 2 |
| **Time to Deploy** | N/A | 1 week | 2 weeks | 3 months |
| **Risk Profile** | Opportunity cost escalates | Human error persists | API dependency | Over-engineering |
| **Reversibility** | N/A | Easy | Moderate | Hard |
| **Dependencies** | None | None | ProPublica API | ProPublica + Schema |
| **12-Month Total Cost** | 780h opportunity | 10h + 24h = 34h | 40h + 48h = 88h | 80h + 24h = 104h |

---

## RECOMMENDATION

**Recommended Option:** [1 / 2 / 3]

**Rationale:** [Explain why this option best balances cost, risk, and impact given our current constraints]

**Example:**
> "Option 2 (Python Script) is recommended. While Option 3 offers full automation, the 3-month development window costs us $390K in opportunity loss (3 months × $130K/month). Option 2 delivers 80% of the value in 2 weeks, allowing us to start processing the backlog immediately. We can upgrade to Option 3 in Q3 2026 if demand justifies it."

**Why Not Other Options?**
- **Option 0 (Do Nothing):** $156K annual opportunity cost is unacceptable
- **Option 1 (Template):** Doesn't reduce manual data entry; scales poorly
- **Option 3 (Full Agent):** 3-month delay costs $390K in lost prospects

---

## OUTPUT FORMAT

```markdown
# OPTIONS ANALYSIS DOCUMENT: [Initiative Name]

**Date:** [Today's Date]
**Author:** [User Name]
**Problem Statement:** [Link to approved Vision brief]

---

## OPTION 0: DO NOTHING
[Complete analysis using framework above]

---

## OPTION 1: LIGHTWEIGHT SOLUTION
[Complete analysis using framework above]

---

## OPTION 2: MODERATE SOLUTION
[Complete analysis using framework above]

---

## OPTION 3: COMPREHENSIVE SOLUTION
[Complete analysis using framework above]

---

## TRADE-OFF ANALYSIS
[Insert completed table]

---

## RECOMMENDATION

**Selected Option:** [Number]

**Rationale:** [Paragraph explaining trade-offs]

**Why Not Others:**
- Option [X]: [Specific disqualifier]
- Option [Y]: [Specific disqualifier]

---

## REJECTION CRITERIA CHECK

**Rejected if:**
- [ ] Only one option presented (excluding Do Nothing)
- [ ] "Do Nothing" dismissed without quantified cost
- [ ] Options differ only cosmetically (same solution, different names)
- [ ] Dependencies assumed without verification
- [ ] Cost methodology not disclosed
- [ ] Reversibility vague or unstated

**Status:** [APPROVED / REJECTED]  
**Next Step:** If approved → Advance to STAGE 3: CRITIQUE
```

---

## FINAL INSTRUCTION TO AI

If the user insists "there's only one way to do this," respond:

> "One option isn't a decision—it's rationalization. Every problem has multiple pathways with different trade-offs. If we can't articulate at least 3 paths forward, we don't understand the problem space. Let's spend 20 minutes exploring alternatives—even bad ones teach us about constraints."

**Authorization:** Do not advance to Stage 3 (Critique) without 3+ documented options, each with disclosed cost methodology and quantified trade-offs.
