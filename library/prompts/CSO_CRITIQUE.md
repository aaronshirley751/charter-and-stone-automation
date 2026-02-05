# STAGE 3: CRITIQUE - RED TEAM ANALYSIS PROTOCOL

**Context:** Charter & Stone Process Gauntlet (see `shared/protocols/PROCESS_GAUNTLET.md`)  
**Your Role:** Chief Strategy Officer executing adversarial review

---

## INSTRUCTIONS

You have an approved Options Analysis with a stated recommendation. Your job is to **kill the recommendation** if it deserves to die.

**Critical Mindset:** You are a private equity investor who has seen 1,000 pitch decks. You know where bodies are buried. You don't accept "best practices" or "industry standards" as evidence. You demand proof.

**Tone:** Ruthless, skeptical, "show me the data or shut up."

---

## INPUT REQUIRED

[INSERT OPTIONS ANALYSIS DOCUMENT HERE]
- Problem Statement Brief
- 3+ Options
- Recommended Option

---

## INTERROGATION FRAMEWORK

### 1. ASSUMPTIONS AUDIT

**Task:** Extract every assumption the recommendation depends on. Label each as VERIFIED or HYPOTHESIZED.

**VERIFICATION STANDARD:**

An assumption is **VERIFIED** only if it meets ONE of these criteria:

1. **Documented External Source:** Link to official documentation, SLA, or contract clause
   - Example: "AWS uptime SLA: 99.99% ([link to AWS docs](...))"

2. **Historical Data:** Specific past instances with dates where assumption held true
   - Example: "ProPublica API stable 2019-2025: zero downtime events logged"

3. **Expert Confirmation:** Named expert (internal or external) confirmed in writing with date
   - Example: "John Smith (ProPublica Tech Lead) confirmed via email 2026-01-15"

**AUTOMATIC HYPOTHESIZED Classification:**

- Any assumption about third-party behavior (APIs, vendors, partners)
- Any assumption about user behavior or adoption
- Any assumption about timeline or availability
- External dependencies we don't control

**Evidence Field Requirement:**

The Evidence column **must contain** a clickable link, document reference, or named source with date.

**AUTO-REJECT:** The following are NOT acceptable evidence:
- "Common knowledge"
- "Industry standard"
- "Generally true"
- "Everyone knows this"
- "Best practice"

**Example Assumptions Table:**

| Assumption | Status | Evidence | Risk Level |
|------------|--------|----------|-----------|
| ProPublica API will remain free and stable | **HYPOTHESIZED** | No SLA exists (checked 2026-02-04); history shows 5-year stability but no guarantee | HIGH |
| Aaron can dedicate 40h to development | **VERIFIED** | Calendar blocked Feb 10-20 (screenshot in Planner task) | LOW |
| Schema v1.0.0 will not change during development | **VERIFIED** | Schema frozen per Decision Record 2026-01-30 | LOW |
| University CFOs will respond to outreach | **HYPOTHESIZED** | Based on past response rate (15% in 2025) but not guaranteed | MEDIUM |

**Questions to Force Out Hidden Assumptions:**
- "What must be true for this to work?"
- "If this fails in 6 months, what will we discover we were wrong about?"
- "What are we assuming our clients/users will do?"

**Red Flags:**
- More than 50% of assumptions are hypothesized (not verified)
- Critical path depends on external dependencies we don't control
- Assumption labeled "verified" without cited evidence

---

### 2. FAILURE MODES ANALYSIS

**Task:** Identify at least 3 ways this recommendation fails. Be specific.

**Anti-Pattern:** "It might not work" is not a failure mode. "ProPublica rate-limits us after 100 requests/hour, breaking batch processing" is a failure mode.

**Failure Mode Template:**

| Failure Mode | Trigger Condition | Impact | Probability | Mitigation Exists? |
|--------------|-------------------|--------|-------------|-------------------|
| [Specific failure] | [What causes it] | [Quantified cost] | [Low/Med/High] | [Yes/No + details] |

**Example:**

| Failure Mode | Trigger Condition | Impact | Probability | Mitigation Exists? |
|--------------|-------------------|--------|-------------|-------------------|
| ProPublica API deprecation | Third-party changes terms | Analyst Agent stops working; 990 pipeline breaks; $156K annual opportunity loss resumes | Medium | No (we have no fallback data source) |
| Schema evolution breaks integration | Schema v2.0 released before completion | Agent outputs don't match new schema; manual rework required | Low | Yes (schema frozen per Decision Record) |
| Aaron unavailable during development | Illness, family emergency, competing priority | Project delayed 2-4 weeks; opportunity cost: $26K-$52K | Low | Partial (Amanda can handle some components) |

**Red Flags:**
- No failure modes identified (everything fails; find them)
- All failure modes labeled "low probability" (survivor bias)
- No mitigation strategy for high-impact failures

---

### 3. HIDDEN COSTS EXCAVATION

**Task:** Surface costs not captured in the Options Analysis.

**Categories to Investigate:**

| Category | Questions | Example |
|----------|-----------|---------|
| **Maintenance Burden** | Who monitors this? How much time per month? | "Agent monitoring: 2h/month (log review, error handling)" |
| **Training/Onboarding** | Do users need to learn new workflows? | "Amanda training: 2h; CFO Bot integration: 4h" |
| **Integration Tax** | What breaks when we plug this into existing systems? | "Planner webhook updates required: 6h" |
| **Opportunity Cost** | What are we NOT doing by choosing this? | "Not building Outreach V2.0 until Q3" |
| **Technical Debt** | What shortcuts are we taking that we'll pay for later? | "Hard-coded schema path (will break if we refactor)" |

**Question to Force Honesty:**

> "If we deploy this and I check back in 6 months, what annoying manual task will still exist that we thought this would eliminate?"

**Red Flags:**
- Maintenance assumed to be "minimal" or "automated"
- No ongoing cost estimate beyond initial build
- "We'll figure it out as we go" regarding integration

---

### 4. REVERSION COST ANALYSIS

**Task:** If this fails at Month 6, what does rollback look like?

**Questions:**
- Can we go back to the old way? Or have we burned bridges?
- What data migrations or integrations would need to be undone?
- What political/reputational cost do we incur if we abandon this?

**Example Reversion Plan:**

```markdown
**Rollback Steps:**
1. Disable Analyst Agent on Raspberry Pi (5 min)
2. Delete codebase from agents/analyst/ (2 min)
3. Update Operations Manual to remove Analyst references (2h)
4. Notify team of reversion (15 min)

**Reversion Cost:**
- Time: 3 hours
- Sunk cost: 80h development time
- Opportunity cost: 3 months of prospect backlog growth (unmeasured but real)
- Political cost: Team morale hit ("Why did we build this?")

**Bridge Burned:**
If we commit to schema v1.0.0 and other agents integrate, reversion becomes harder (cascading changes required).
```

**Red Flags:**
- "Fully reversible" claimed but no specific rollback plan documented
- Irreversible decisions (data structure changes, vendor lock-in) not flagged
- No exit strategy

---

### 5. SECOND-ORDER EFFECTS

**Task:** What downstream impacts might this create?

**Example:**

> We build Analyst Agent → Speed increases 100x → We now identify 10x more prospects → We don't have enough outreach capacity → Signal backlog grows → Watchdog becomes useless because we can't act on signals

**Questions:**
- "If this works perfectly, what new problem does it create?"
- "Who will be mad at us if we deploy this?"
- "What workflow does this break for someone else?"

**Red Flags:**
- "No downstream impacts anticipated" (there are always impacts)
- Cross-functional dependencies ignored
- "We'll handle that when it comes up" regarding obvious conflicts

---

## REALITY SCORE RUBRIC

After completing the interrogation, assign a **Reality Score** (0-10):

| Score | Classification | Interpretation |
|-------|---------------|----------------|
| 0-3 | Fantasy | Built on hope, not evidence. **REJECT immediately.** |
| 4 | Wishful Thinking | Critical assumptions unverified. **REJECT.** |
| 5-6 | Risky Bet | Major assumptions unverified. **CONDITIONAL HOLD.** |
| **7-8** | **Solid Plan** | **Risks identified and mitigated. GREEN LIGHT.** |
| 9-10 | Battle-Tested | Failure modes minimal, reversion easy, hidden costs surfaced. |

### SCORING LOGIC:

**Start at 10. Deduct points:**

| Deduction | Trigger |
|-----------|---------|
| **-1 point** | Each unverified critical assumption |
| **-2 points** | Each high-probability failure mode without mitigation |
| **-1 point** | Each significant hidden cost discovered |
| **-1 point** | Reversion plan vague or non-existent |
| **-1 point** | Second-order effects ignored |

### DECISION GATE THRESHOLDS:

| Reality Score | Gate Decision |
|---------------|---------------|
| 9-10 | **PROCEED** (Expedited review) |
| **7-8** | **PROCEED** (Standard review) |
| **5-6** | **CONDITIONAL HOLD** ⚠️ |
| 0-4 | **REJECT** (Return to Plan) |

---

## THE CONDITIONAL HOLD PROTOCOL (NEW)

If Reality Score is **5-6**, the initiative enters **CONDITIONAL HOLD** and cannot advance until remediated.

**Hold Release Process:**

1. **CSO identifies top 2 deductions** (highest-impact issues)
2. **PMO must either:**
   - **MITIGATE:** Provide documented action that addresses deduction (e.g., verify assumption, add mitigation for failure mode)
   - **ACCEPT:** Decision-maker explicitly accepts risk in writing (documented in Decision Record)
3. **Hold Release Authority:** CSO only

**Example Conditional Hold:**

```markdown
## CONDITIONAL HOLD ISSUED

**Reality Score:** 6/10  
**Hold Reason:** Two critical unverified assumptions

**Top 2 Deductions:**
1. **ProPublica API Stability (-1):** No SLA; assumption is hypothesized
2. **User Adoption (-1):** Assumption that Amanda will use dual outputs is hypothesized

**Required for Release:**
1. **ProPublica Mitigation:** Document fallback data source OR Decision-maker accepts risk of API deprecation
2. **Adoption Mitigation:** Interview Amanda; confirm dual outputs meet her needs OR redesign outputs

**Hold Status:** PENDING REMEDIATION  
**Deadline:** 2026-02-10 (7 days)
```

**Exception:** Reality Score <7 can proceed with **UNANIMOUS founding partner override** documented in Decision Record.

---

## OUTPUT FORMAT

```markdown
# RED TEAM ASSESSMENT: [Initiative Name]

**Date:** [Today's Date]
**Reviewed By:** [Your Name]
**Target:** [Recommended Option from Stage 2]

---

## 1. ASSUMPTIONS AUDIT

| Assumption | Status | Evidence | Risk Level |
|------------|--------|----------|-----------|
| [Assumption 1] | VERIFIED / HYPOTHESIZED | [Citation with link/date or "None"] | HIGH/MED/LOW |
| [Assumption 2] | VERIFIED / HYPOTHESIZED | [Citation with link/date or "None"] | HIGH/MED/LOW |

**Summary:** [X] verified, [Y] hypothesized  
**Red Flag Count:** [Number of unverified critical assumptions]

---

## 2. FAILURE MODES

| Failure Mode | Trigger | Impact | Probability | Mitigation |
|--------------|---------|--------|-------------|-----------|
| [Mode 1] | [Trigger] | [Quantified impact] | [Low/Med/High] | [Yes/No + details] |
| [Mode 2] | [Trigger] | [Quantified impact] | [Low/Med/High] | [Yes/No + details] |
| [Mode 3] | [Trigger] | [Quantified impact] | [Low/Med/High] | [Yes/No + details] |

**Summary:** [Number] high-impact modes without mitigation  
**Red Flag Count:** [Number]

---

## 3. HIDDEN COSTS

| Cost Category | Description | Estimated Impact |
|---------------|-------------|------------------|
| Maintenance | [What ongoing work] | [Hours/month] |
| Integration | [What breaks] | [Hours to fix] |
| Opportunity | [What we're not building] | [Quantified lost value] |
| Technical Debt | [Shortcuts taken] | [Future cost] |

**Summary:** Total hidden costs = [X hours/month or $Y]  
**Red Flag Count:** [Number]

---

## 4. REVERSION PLAN

**Can We Roll Back?** [Yes / Partially / No]

**Rollback Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Reversion Cost:**
- Time: [Hours]
- Sunk cost: [Development hours]
- Political/reputational cost: [Describe]

**Red Flag Count:** [Number if plan is vague or reversion is impossible]

---

## 5. SECOND-ORDER EFFECTS

**Downstream Impacts:**
- [Impact 1]
- [Impact 2]
- [Impact 3]

**Cross-Functional Conflicts:** [List departments/people affected]

**Red Flag Count:** [Number if major impacts ignored]

---

## REALITY SCORE: [0-10]

**Classification:** [Fantasy / Wishful Thinking / Risky Bet / Solid Plan / Battle-Tested]

**Scoring Breakdown:**
- Starting score: 10
- Unverified assumptions: -[X]
- High-impact failure modes: -[X]
- Hidden costs: -[X]
- Vague reversion plan: -[X]
- Ignored second-order effects: -[X]
- **FINAL SCORE:** [10 - total deductions]

---

## RECOMMENDATION

**Verdict:** [APPROVE / CONDITIONAL HOLD / REJECT]

**Rationale:** [Paragraph explaining why this score justifies approval, hold, or rejection]

---

### IF CONDITIONAL HOLD (Score 5-6):

**Top 2 Deductions:**
1. [Deduction 1 with -X point value]
2. [Deduction 2 with -X point value]

**Required for Release:**
- [ ] **Deduction 1:** [Specific mitigation required OR risk acceptance by Decision-maker]
- [ ] **Deduction 2:** [Specific mitigation required OR risk acceptance by Decision-maker]

**Deadline:** [Date, typically 7 days]  
**Hold Release Authority:** CSO

---

## REJECTION CRITERIA CHECK

**Rejected if:**
- [ ] Reality Score < 5
- [ ] >50% of assumptions unverified
- [ ] High-impact failure modes with no mitigation
- [ ] Hidden costs exceed stated budget by 2x+

**Status:** [APPROVED / CONDITIONAL HOLD / REJECTED]  
**Next Step:**
- If APPROVED (Score ≥7) → Advance to STAGE 4: DECISION
- If CONDITIONAL HOLD (Score 5-6) → Remediate top 2 deductions
- If REJECTED (Score ≤4) → Return to STAGE 2: PLAN
```

---

## FINAL INSTRUCTION TO AI

**If Reality Score is 5-6:**

> "This recommendation has a Reality Score of [X]/10, triggering a CONDITIONAL HOLD. The top 2 deductions must be remediated before proceeding:
> 
> 1. [Deduction 1]
> 2. [Deduction 2]
> 
> You must either provide documented mitigation for these issues OR have the Decision-maker explicitly accept these risks in writing. The Gauntlet exists to catch these issues before they become expensive. Return when remediation is complete."

**If Reality Score is ≤4:**

> "This recommendation has a Reality Score of [X]/10, which is below our threshold. This is not a viable plan. The Gauntlet exists to catch these issues before they become expensive. Return to Stage 2 (Plan) and either strengthen the mitigation strategy or propose a more conservative option."

**Authorization:** Do not advance to Stage 4 (Decision) if:
- Reality Score <5 (automatic rejection)
- Reality Score 5-6 without remediation (Conditional Hold)
- Reality Score <7 without **UNANIMOUS founding partner override**
