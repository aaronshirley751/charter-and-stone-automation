# THE PROCESS GAUNTLET
## Charter & Stone Doctrine of Evidence
**Version:** 1.1  
**Status:** Canonical  
**Last Updated:** February 4, 2026  
**Last Audit:** February 4, 2026 (Red Team Review — PASS WITH PATCHES)  
**Classification:** Internal Operations Protocol

---

## PREAMBLE: WHY WE EXIST

### The Disease

Most consultants are vendors in disguise. They arrive with slide decks pre-loaded, recommendations pre-written, and "discovery phases" designed to bill hours while confirming what they already planned to sell you.

The consulting industry has become an elaborate theater of activity—process frameworks, stakeholder interviews, SWOT matrices, and strategy documents that collect dust in SharePoint folders. The client pays for motion. They receive no forward progress.

Charter & Stone exists to kill this disease.

### The Cure: Evidence Over Activity

We do not worship process. We demand evidence.

Every recommendation must answer one question: **"What did you measure, and what did the measurement tell you?"**

If you cannot answer that question, you are not consulting. You are guessing with confidence. Our clients can guess for free.

### The Anti-Vendor Commitment

We make three promises:

1. **We do not sell solutions looking for problems.** We diagnose first. We prescribe second. If the diagnosis reveals you don't need us, we tell you.

2. **We do not confuse troubleshooting with system design.** Fixing today's symptom is not the same as building tomorrow's infrastructure. We will not let you pay us for the former while pretending it's the latter.

3. **We do not hide behind "best practices."** Best practices are averages. Your institution is not average. If our recommendation sounds like something you could have read in a Harvard Business Review article, we have failed you.

### The Lesson That Forged This Doctrine

This document exists because we learned the hard way: **Troubleshooting is not System Design.**

When a system fails, the instinct is to fix it. Debug the code. Restart the service. Patch the workflow. The immediate problem disappears, and everyone exhales.

But the underlying architecture remains unchanged. The same failure mode waits in the shadows, ready to manifest again—usually at a less convenient time, usually with higher stakes.

The Gauntlet exists to force separation between reactive fixes and proactive construction. If you're troubleshooting, say so. If you're building, prove it. The two are not interchangeable, and this protocol ensures we never confuse them again.

---

## THE SIX STAGES

Every initiative—internal or client-facing—must traverse the Gauntlet. There are no shortcuts. There are no exceptions for "quick wins" or "obvious solutions."

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   VISION → PLAN → CRITIQUE → DECISION → ARCHITECTURE → EXECUTION│
│     ↑                                                     ↓     │
│     │                                                     │     │
│     └──────────────── KILL SWITCH ────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Any stage can trigger a rejection. Rejection returns the initiative to Vision for re-scoping or termination.

---

### STAGE 1: VISION
**The Problem Definition**

**Purpose:** Establish what we are solving and why it matters. Not what we are building—what pain we are eliminating.

**Entry Criteria:**
- A stated problem exists (verbal or written)
- At least one stakeholder has expressed the problem
- The problem has not already been solved by existing infrastructure

**Required Deliverable:** Problem Statement Brief

The Problem Statement must answer:

| Question | Requirement |
|----------|-------------|
| **What is the observable symptom?** | Specific, measurable behavior (not "things feel slow") |
| **Who experiences the symptom?** | Named roles or personas |
| **What is the impact?** | Quantified cost: time, money, risk, or opportunity |
| **What is the root cause hypothesis?** | Our current best guess (explicitly labeled as hypothesis) |
| **What would "solved" look like?** | Observable, measurable success criteria |

**Exit Criteria:**
- Problem Statement Brief approved by initiative owner
- Impact quantified (even if estimated)
- No conflation of symptoms with solutions

**Red Flags That Trigger Rejection:**
- "We need to build [X]" appears before the problem is defined
- Impact cannot be articulated beyond "it would be nice"
- The problem statement describes a solution in disguise
- Multiple unrelated problems bundled into one initiative

---

### STAGE 2: PLAN
**The Tactical Options**

**Purpose:** Generate multiple pathways to solve the defined problem. Not one solution—plural options with trade-off analysis.

**Entry Criteria:**
- Approved Problem Statement Brief from Vision
- No predetermined solution has been mandated

**Required Deliverable:** Options Analysis Document

The Options Analysis must include:

| Component | Requirement |
|-----------|-------------|
| **Minimum 3 Options** | Including "Do Nothing" as Option 0 |
| **Cost Estimate per Option** | Time, money, opportunity cost |
| **Risk Profile per Option** | What could go wrong? What's the blast radius? |
| **Reversibility Assessment** | Can we undo this if wrong? At what cost? |
| **Dependencies** | What must exist before this option is viable? |
| **Recommendation** | Stated preference with explicit reasoning |

**Exit Criteria:**
- Three or more options documented
- Trade-offs articulated for each option
- "Do Nothing" option honestly evaluated with **quantified cost of inaction**
- Recommendation stated with rationale

**Red Flags That Trigger Rejection:**
- Only one option presented ("there's really only one way to do this")
- "Do Nothing" dismissed without cost analysis
- Options differ only cosmetically (same solution, three names)
- Dependencies hand-waved or assumed to exist

---

### STAGE 3: CRITIQUE
**The Red Team Analysis**

**Purpose:** Adversarial stress-testing of the recommended option. The goal is to find fatal flaws before we commit resources.

**Entry Criteria:**
- Options Analysis Document with stated recommendation
- Critique team has no vested interest in the recommendation's success

**Required Deliverable:** Red Team Assessment

The Critique must examine:

| Vector | Questions |
|--------|-----------|
| **Assumptions** | What must be true for this to work? Are those assumptions verified or hoped? |
| **Failure Modes** | How does this fail? What's the worst-case scenario? |
| **Hidden Costs** | What ongoing maintenance, support, or attention does this require? |
| **Opportunity Cost** | What are we NOT doing by committing to this? |
| **Reversion Cost** | If this fails at month 6, what does rollback look like? |
| **Second-Order Effects** | What downstream impacts might this create? |

**Exit Criteria:**
- All major assumptions identified and categorized (verified vs. hypothesized)
- At least three failure modes documented
- Hidden costs surfaced and added to cost estimate
- Reversion plan sketched

**Red Flags That Trigger Rejection:**
- Critique is perfunctory ("looks good to me")
- No failure modes identified (everything fails; find the failure modes)
- Assumptions labeled "verified" without evidence
- Critique performed by the same person who authored the plan

---

### STAGE 4: DECISION
**The Authorization Gate**

**Purpose:** Formal commitment of resources. This is the point of no return for preliminary work.

**Entry Criteria:**
- Problem Statement Brief (approved)
- Options Analysis Document (complete)
- Red Team Assessment (adversarial)
- Decision-maker identified and available

**Required Deliverable:** Decision Record

The Decision Record must contain:

| Field | Requirement |
|-------|-------------|
| **Decision** | Proceed / Reject / Defer |
| **Selected Option** | Which option, explicitly named |
| **Rationale** | Why this option over alternatives |
| **Accepted Risks** | Which risks are we knowingly taking? |
| **Success Criteria** | How will we know this worked? (Measurable) |
| **Review Trigger** | When do we re-evaluate? (Time or condition) |
| **Owner** | Single accountable human |
| **Resource Allocation** | What are we committing? |

**Exit Criteria:**
- Decision formally recorded
- Owner assigned and acknowledged
- Resources allocated or reserved
- Success criteria are measurable, not subjective

**Red Flags That Trigger Rejection:**
- "Let's just try it and see" without defined success criteria
- No single owner (shared accountability = no accountability)
- Decision made without reviewing Red Team Assessment
- Success criteria are vibes ("it feels better")

---

### STAGE 5: ARCHITECTURE
**The Technical Blueprint**

**Purpose:** Translate the approved decision into a buildable specification. This is design, not implementation.

**Entry Criteria:**
- Approved Decision Record
- Technical resources identified
- No implementation has begun

**Required Deliverable:** Technical Blueprint

The Architecture specification must include:

| Component | Requirement |
|-----------|-------------|
| **Context & Objective** | Link to Problem Statement; why this design solves it |
| **File System Target** | Where does this live in the repo/infrastructure? |
| **I/O Contract** | Inputs, outputs, data formats, schema compliance |
| **Logic Flow** | Pseudocode or flowchart (NOT implementation code) |
| **Dependencies** | External systems, libraries, APIs, data sources |
| **Integration Points** | How does this connect to existing infrastructure? |
| **The "Brain"** | For AI agents: the system prompt, verbatim |
| **Test Criteria** | How do we verify this works before deployment? |

**Exit Criteria:**
- Blueprint reviewed by someone other than the author
- I/O contracts explicitly defined
- No ambiguity in "what success looks like" for implementation
- Test criteria defined before code is written

**Red Flags That Trigger Rejection:**
- Architecture is actually implementation (code submitted instead of spec)
- I/O contracts vague or "to be determined"
- Integration points hand-waved ("it'll connect to the existing system")
- No test criteria ("we'll know it works when we see it")

---

### STAGE 6: EXECUTION
**The Implementation**

**Purpose:** Build the thing. This is the only stage where code is written, infrastructure is provisioned, or changes are deployed.

**Entry Criteria:**
- Approved Technical Blueprint
- Test criteria defined
- Rollback plan documented
- Owner confirmed

**Required Deliverable:** Deployed Capability + Execution Log

The Execution must produce:

| Artifact | Requirement |
|----------|-------------|
| **Working Implementation** | Matches the Blueprint specification |
| **Test Results** | Evidence that test criteria were met |
| **Execution Log** | What was done, when, by whom, any deviations from plan |
| **Documentation Update** | Operations Manual or relevant docs updated |
| **Handover Brief** | If ongoing maintenance required, who owns it now? |

**Exit Criteria:**
- Implementation matches Blueprint (or deviations documented and approved)
- Tests pass
- Documentation updated
- Ownership transferred (if applicable)

**Red Flags That Trigger Rejection:**
- Implementation diverges from Blueprint without documented approval
- "It works on my machine" without reproducible test evidence
- Documentation not updated ("I'll do it later")
- No clear owner for ongoing maintenance

---

## THE KILL SWITCH

Any stage can trigger rejection. Rejection is not failure—it is the system working.

### Rejection Triggers

| Trigger | Response |
|---------|----------|
| **Problem Statement invalid** | Return to Vision; re-scope or terminate |
| **No viable options** | Return to Vision; problem may be mis-framed |
| **Critique reveals fatal flaw** | Return to Plan; generate new options |
| **Decision blocked** | Hold at Decision; escalate or defer |
| **Architecture unimplementable** | Return to Decision; may need different option |
| **Execution fails tests** | Return to Architecture; design flaw likely |

### The Rejection Record

Every rejection must be documented:

```markdown
## REJECTION RECORD

**Initiative:** [Name]
**Stage:** [Where rejection occurred]
**Date:** [When]
**Rejected By:** [Who — must be named role with kill authority]
**Reason:** [Specific trigger]
**Return To:** [Which stage]
**Required Action:** [What must change before re-submission]
```

Rejections are victories. Every killed initiative is resources we didn't waste. If your project can't survive the Gauntlet, it couldn't survive the market.

---

## OPERATING PRINCIPLES

### 1. Evidence Over Authority
The most senior person in the room does not win arguments. The person with the best evidence wins. If you cannot produce evidence, your opinion is noted and weighted accordingly.

### 2. Troubleshooting ≠ System Design
Fixing a bug is not building infrastructure. If you are in firefighting mode, acknowledge it. Do not dress up reactive work as strategic investment. They are different activities with different values.

### 3. The "Do Nothing" Option Is Always Valid
Every initiative competes against inaction. If "Do Nothing" is not honestly evaluated with a **quantified cost of inaction**, the analysis is incomplete. Sometimes the right answer is to wait, watch, or walk away.

### 4. Single-Threaded Ownership
Every initiative has one owner. Not a committee. Not "shared responsibility." One human whose name is on the Decision Record. Committees diffuse accountability; individuals concentrate it.

### 5. Measure Before Acting
If you cannot measure the problem, you cannot verify the solution. Intuition is valuable for generating hypotheses. It is insufficient for validating results.

### 6. Reversibility Is a Feature
Prefer decisions that can be undone. When irreversible decisions are required, they demand proportionally more scrutiny. The cost of being wrong should inform the rigor of the process.

### 7. Authority Hierarchy (Non-Negotiable)

The Gauntlet requires clear kill authority. Without it, governance is theater.

**Kill Authority by Stage:**

| Stage | Kill Authority | Scope |
|-------|---------------|-------|
| Vision | Initiative Owner | Can reject malformed problem statements |
| Plan | PMO Director | Can reject insufficient options analysis |
| **Critique** | **CSO** | **Unilateral veto power on recommendations** |
| **Decision** | **CSO** | **Unilateral veto power on resource commitment** |
| Architecture | Lead Engineer | Can reject unbuildable specifications |
| Execution | Owner | Can reject failed implementations |

**CSO Veto Authority (Stages 3-4):**

The Chief Strategy Officer holds unilateral veto power at Critique and Decision stages. A CSO "REJECT" verdict cannot be overridden except by **UNANIMOUS founding partner agreement**, documented in the Decision Record with explicit rationale for override.

**Escalation Protocol:**

If CSO and PMO disagree at the Decision stage:
1. Matter escalates to founding partners within **48 hours**
2. Both CSO and PMO submit written position statements
3. Founding partners render binding decision within **72 hours**
4. **Silence = rejection by default** (no decision = no proceed)

**Override Requirements:**

A founding partner cannot unilaterally waive Gauntlet requirements. Waiver requires:
- Both founding partners' signatures
- Written rationale explaining why the Gauntlet stage is being bypassed
- Explicit acceptance of risks that the bypassed stage would have surfaced
- Documentation in the Decision Record (permanent audit trail)

---

## OPERATIONAL TOOLING

Each Gauntlet stage has a corresponding **Prompt Template** that operationalizes the requirements:

| Stage | Prompt Template | Purpose |
|-------|-----------------|---------|
| Vision | `library/prompts/PMO_VISION.md` | Problem Definition Protocol |
| Plan | `library/prompts/PMO_PLAN.md` | Options Analysis Protocol |
| Critique | `library/prompts/CSO_CRITIQUE.md` | Red Team Analysis Protocol |
| Decision | `library/prompts/CSO_DECISION.md` | Authorization Gate Protocol |
| Architecture | `library/prompts/ARCHITECT_BLUEPRINT.md` | Technical Blueprint Protocol |

**Binding Requirement:** All Gauntlet stages must use the corresponding prompt template. Freeform submissions that bypass the template structure are auto-rejected.

The prompts are not suggestions. They are the operational implementation of this Constitution.

---

## ANTI-PATTERNS: WHAT THE GAUNTLET PREVENTS

| Anti-Pattern | What It Looks Like | How The Gauntlet Stops It |
|--------------|--------------------|-----------------------------|
| **Solution-First Thinking** | "We need Salesforce" before defining the problem | Vision stage demands problem statement before solutions |
| **Analysis Paralysis** | Endless planning, no commitment | Decision stage forces authorization or rejection |
| **Scope Creep** | Initiative grows to absorb adjacent problems | Problem Statement defines boundaries; deviations require new initiative |
| **Vaporware Architecture** | Designs that can't be built | Architecture requires I/O contracts and test criteria |
| **Cowboy Implementation** | Building without spec | Execution requires approved Blueprint |
| **Sunk Cost Escalation** | "We've come too far to stop" | Kill Switch can be triggered at any stage |
| **Accountability Diffusion** | "The team decided" | Decision Record requires single owner |
| **Authority Theater** | Process without enforcement | CSO veto authority with explicit override requirements |

---

## APPENDIX A: QUICK REFERENCE

### Stage Sequence
```
1. VISION       → Problem Statement Brief
2. PLAN         → Options Analysis Document  
3. CRITIQUE     → Red Team Assessment
4. DECISION     → Decision Record
5. ARCHITECTURE → Technical Blueprint
6. EXECUTION    → Deployed Capability + Execution Log
```

### Kill Authority Quick Reference
```
Stages 1-2:  PMO Director can reject
Stages 3-4:  CSO has unilateral veto (override requires unanimous founding partners)
Stage 5:     Lead Engineer can reject
Stage 6:     Owner can reject
```

---

## APPENDIX B: ACCELERATED TRACK

**This section replaces "Minimum Viable Gauntlet."**

For initiatives meeting **ALL** of the following criteria:
- Estimated work <4 hours
- Fully reversible (rollback cost <1 hour AND no external dependencies created)
- No external stakeholder impact
- No budget allocation >$100
- Does not touch production systems
- Does not create new external-facing outputs
- Requires only one person

**Accelerated Process:**

| Stage | Accelerated Requirement |
|-------|------------------------|
| Vision | 1-paragraph problem statement with **quantified impact** (numbers required, not vibes) |
| Plan | 2 options with trade-off comparison (not just listing); "Do Nothing" must have quantified cost |
| **Critique** | **Peer review by ANY team member who did NOT author the plan** (self-review prohibited) |
| Decision | Verbal approval logged in Planner task with **24-hour review trigger** |
| Architecture | Inline in task description |
| Execution | Standard |

**Self-Review Is Prohibited.** The Critique stage exists specifically to bring adversarial perspective. A person reviewing their own work is journaling, not critiquing.

**Disqualifying Conditions (Auto-Escalate to Full Gauntlet):**

If ANY of the following become true during execution:
- Initiative touches production systems
- Initiative creates new external-facing outputs
- Initiative requires more than 1 person
- Estimated work exceeds 2 hours after starting
- Any dependency on external party emerges

The initiative immediately escalates to full Gauntlet process. Do not continue under Accelerated Track.

---

## DOCUMENT HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-04 | Aaron Shirley / Claude (CSO) | Initial doctrine |
| **1.1** | **2026-02-04** | **Claude (CSO)** | **Red Team patches: Added Operating Principle #7 (Authority Hierarchy), replaced "Minimum Viable Gauntlet" with "Accelerated Track", prohibited self-review, added Operational Tooling cross-reference, tone hardening ("rejections are victories"), added CSO veto authority, added escalation protocol** |

---

## RATIFICATION

This document is the operational constitution of Charter & Stone. Adherence is not optional.

Waiver of any Gauntlet requirement requires:
- Both founding partners' signatures
- Written rationale
- Explicit risk acceptance
- Permanent documentation in the Decision Record

The Gauntlet is the price of being right.

---

**END OF DOCTRINE**
