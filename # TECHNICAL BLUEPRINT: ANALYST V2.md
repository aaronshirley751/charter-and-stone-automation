# TECHNICAL BLUEPRINT: ANALYST V2.0-LITE API CONNECTIVITY DEBUG (PHASE 6.5)

**Blueprint Date**: February 3, 2026  
**Architect**: Chief Systems Architect  
**Authorization Source**: `ARCHITECT_HANDOFF_API_DEBUG_AUTHORIZATION.md`, `PMO_CSO_AUTHORIZATION_SUMMARY.md`  
**Status**: 🔴 **CRITICAL PATH BLOCKER**  
**Priority**: **P0 — PRODUCTION BLOCKER**

---

## SECTION 1: CONTEXT & OBJECTIVE

### What Is This?

Phase 6 Integration Testing revealed a **critical production blocker**: the Perplexity MCP server integration is non-functional due to authentication and API connectivity issues. The Albright College smoke test passed **only because mock data was used** when API keys were unavailable—the real Perplexity API was never successfully called.

### Why Are We Building This?

**Strategic Impact**: Without functional Perplexity integration, V2.0-LITE cannot deliver real-time intelligence. The system degrades to V1-only mode, eliminating our 18-24 month competitive advantage and invalidating the entire OPERATION SNIPER value proposition.

**Business Impact**:
- **21-university backlog**: Cannot be processed with V2 intelligence
- **Gate 2 (5-university batch)**: Blocked until API connectivity restored
- **Production deployment**: Cannot proceed until real API calls validated
- **CSO code review (Feb 4, 10am)**: Must demonstrate live API functionality

### Root Cause Analysis

From `ARCHITECT_HANDOFF_API_DEBUG_AUTHORIZATION.md`:

1. **MCP Server Architecture**: Custom Perplexity MCP server exists but may have authentication issues
2. **Dual API Access**: System has both direct Perplexity API capability AND MCP server integration
3. **Mock Fallback**: Test passed with mocked data, masking real API failure
4. **Environment Configuration**: Unclear which API keys/endpoints are required and where

**Critical Discovery**: The Engineer reported success, but Architect review revealed the smoke test never made real API calls—it used mock data when `PERPLEXITY_API_KEY` was missing.

---

## SECTION 2: STRATEGIC DECISION — MCP vs DIRECT API

### The Two Paths Forward

#### PATH A: FIX MCP SERVER (Higher Complexity)
**Pros**:
- Consistent with broader Digital Teammates infrastructure
- Enables MCP-based orchestration patterns
- Future-proofs for multi-agent coordination

**Cons**:
- Unknown debugging time (MCP server code needs audit)
- Authentication flow complexity (OAuth? API keys?)
- Dependency on external MCP server stability

**Estimated Time**: 4-8 hours (uncertain)

---

#### PATH B: USE DIRECT PERPLEXITY API (Lower Complexity) ⭐ **RECOMMENDED**
**Pros**:
- **Already implemented** in `recon.py` (163 lines production code)
- Simple authentication (API key in environment variable)
- Proven stability (Perplexity REST API is production-grade)
- Fast validation (can test in <30 minutes)

**Cons**:
- Bypasses MCP infrastructure (tactical vs strategic)
- May need to revisit if MCP integration becomes critical later

**Estimated Time**: 30 minutes to 1 hour

---

### Architect's Recommendation: **PATH B (DIRECT API)**

**Rationale**:
1. **Time-Critical**: Gate 2 timeline is compressed (Feb 5-6 production deployment)
2. **Risk Mitigation**: Direct API reduces dependencies and failure points
3. **Proven Code**: `recon.py` already has production-ready Perplexity client
4. **Validation Speed**: Can test live API calls in <30 minutes
5. **Tactical Win**: Unblock Gate 2 now, revisit MCP integration in Phase 7+

**Strategic Note**: This is a **tactical pivot**, not abandoning MCP. Once V2.0-LITE is production-stable, we can add MCP integration as enhancement in future sprint.

---

## SECTION 3: FILE SYSTEM TARGET

### Current State (From Implementation Manifest)
```
agents/analyst/sources/v2_lite/
├── __init__.py              (24 lines)
├── recon.py                 (163 lines) ← CONTAINS DIRECT API CLIENT
├── synthesis.py             (234 lines)
└── classification.py        (152 lines)

agents/analyst/core/
├── orchestrator.py          (305 lines)
└── __init__.py              (10 lines)

tests/integration/
├── test_albright_smoke.py   ← CURRENTLY USING MOCKS
└── test_v2_resilience.py
```

### Target Changes (Minimal Modifications)
```
agents/analyst/sources/v2_lite/
└── recon.py                 ← VERIFY/FIX: Direct API authentication

tests/integration/
└── test_albright_smoke.py   ← REMOVE MOCKS, USE REAL API

.env (NEW or UPDATED)
└── PERPLEXITY_API_KEY=xxx   ← CRITICAL: Must be set

docs/ (NEW)
└── API_SETUP_GUIDE.md       ← User-facing documentation
```

**No new modules required.** This is a **configuration and validation fix**, not new feature development.

---

## SECTION 4: DEBUGGING PROTOCOL

### Phase 1: Environment Validation (15 minutes)

**Objective**: Confirm API key is properly configured and accessible.

**Steps**:
1. **Locate API Key**:
   ```bash
   # Check environment variables
   echo $PERPLEXITY_API_KEY
   
   # Check .env file
   cat .env | grep PERPLEXITY_API_KEY
   
   # Check if key is set in current shell
   python -c "import os; print('Key exists:', 'PERPLEXITY_API_KEY' in os.environ)"
   ```

2. **Validate Key Format**:
   - Perplexity API keys typically start with `pplx-` prefix
   - Length: ~40-60 characters
   - Example: `pplx-1234567890abcdef1234567890abcdef12345678`

3. **Test API Connectivity**:
   ```python
   # Quick connectivity test (run in Python REPL)
   import os
   import requests
   
   api_key = os.getenv('PERPLEXITY_API_KEY')
   if not api_key:
       print("ERROR: PERPLEXITY_API_KEY not set")
   else:
       print(f"Key found: {api_key[:10]}...")
       
       # Test API endpoint
       response = requests.post(
           'https://api.perplexity.ai/chat/completions',
           headers={
               'Authorization': f'Bearer {api_key}',
               'Content-Type': 'application/json'
           },
           json={
               'model': 'sonar-pro',
               'messages': [{'role': 'user', 'content': 'test'}]
           }
       )
       
       print(f"Status: {response.status_code}")
       if response.status_code == 200:
           print("✅ API connectivity confirmed")
       else:
           print(f"❌ API error: {response.text}")
   ```

**Success Criteria**:
- ✅ `PERPLEXITY_API_KEY` environment variable is set
- ✅ API key format is valid (starts with `pplx-`)
- ✅ Test API call returns 200 status code

**Failure Triggers**:
- ❌ Key not found in environment → **SET KEY IMMEDIATELY**
- ❌ Key format invalid → **GET NEW KEY FROM PERPLEXITY DASHBOARD**
- ❌ API returns 401 (unauthorized) → **KEY IS INVALID/EXPIRED**
- ❌ API returns 429 (rate limit) → **WAIT OR UPGRADE PLAN**

---

### Phase 2: Recon Module Audit (15 minutes)

**Objective**: Verify `recon.py` is correctly configured for direct API access.

**Review Checklist**:

```python
# agents/analyst/sources/v2_lite/recon.py

class PerplexityReconClient:
    def __init__(self, api_key: Optional[str] = None):
        # ✅ CHECK: Does constructor accept api_key parameter?
        # ✅ CHECK: Does it fall back to os.getenv('PERPLEXITY_API_KEY')?
        
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        
        # ❌ BLOCKER: If api_key is None, should raise ValueError
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment")
    
    def _call_perplexity(self, query: str, max_results: int = 5) -> Dict:
        # ✅ CHECK: Is this method using requests.post to Perplexity API?
        # ✅ CHECK: Is Authorization header formatted correctly?
        # ✅ CHECK: Is error handling present for network failures?
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # ❌ COMMON BUG: Check endpoint URL is correct
        endpoint = 'https://api.perplexity.ai/chat/completions'  # Correct
        # NOT: 'https://api.perplexity.com/...' (wrong domain)
        
        # ❌ COMMON BUG: Check model name is valid
        model = 'sonar-pro'  # Correct for search
        # NOT: 'gpt-4' or 'claude-3' (wrong provider)
```

**Expected Code Patterns**:
```python
# CORRECT: Direct API call
response = requests.post(
    'https://api.perplexity.ai/chat/completions',
    headers={'Authorization': f'Bearer {self.api_key}'},
    json={'model': 'sonar-pro', 'messages': [...]},
    timeout=30
)

# INCORRECT: MCP server call (not using direct API)
response = mcp_client.call_tool('perplexity_search', {'query': query})
```

**Validation Steps**:
1. Open `agents/analyst/sources/v2_lite/recon.py`
2. Confirm `PerplexityReconClient` uses `requests.post` (not MCP)
3. Confirm endpoint URL is `https://api.perplexity.ai/chat/completions`
4. Confirm model is `sonar-pro` or `sonar` (not other provider models)
5. Confirm error handling catches `requests.exceptions.RequestException`

**Red Flags**:
- ❌ Import statement includes `mcp` or `anthropic.mcp`
- ❌ Method calls `mcp_client.call_tool()`
- ❌ Endpoint URL is not `api.perplexity.ai`
- ❌ No error handling for network timeouts

---

### Phase 3: Remove Test Mocks (10 minutes)

**Objective**: Ensure smoke test uses real API, not mock data.

**File**: `tests/integration/test_albright_smoke.py`

**Current Problem** (from handoff doc):
```python
# INCORRECT: Test passes with mocks when API key missing
@patch('agents.analyst.sources.v2_lite.recon.PerplexityReconClient._call_perplexity')
def test_albright_smoke(mock_perplexity):
    mock_perplexity.return_value = {...}  # Mock data
    # Test passes but never validates real API
```

**Required Fix**:
```python
# CORRECT: Test fails fast if API key missing
def test_albright_smoke():
    # NO MOCKS — real API calls only
    
    # Fail fast if key not configured
    if not os.getenv('PERPLEXITY_API_KEY'):
        pytest.skip("PERPLEXITY_API_KEY not set — cannot test live API")
    
    # Run real end-to-end test
    result = enhance_profile_with_v2_lite(...)
    
    # Validate real API was called
    assert result['metadata']['intelligence_queries_used'] == 3
    assert result['v2_signals']['composite_score'] > 0
```

**Changes Required**:
1. **Remove all `@patch` decorators** for Perplexity/Claude API calls
2. **Add API key check** at test start (fail fast if missing)
3. **Add `pytest.mark.integration`** decorator (requires real API)
4. **Add timeout** (tests should complete in <60 seconds)

**Updated Test Structure**:
```python
import pytest
import os

@pytest.mark.integration  # Mark as integration test (requires API)
def test_albright_smoke():
    """
    LIVE API TEST — No mocks allowed.
    Requires: PERPLEXITY_API_KEY, ANTHROPIC_API_KEY set in environment.
    """
    
    # Gate 1: Environment check
    if not os.getenv('PERPLEXITY_API_KEY'):
        pytest.skip("PERPLEXITY_API_KEY not set")
    if not os.getenv('ANTHROPIC_API_KEY'):
        pytest.skip("ANTHROPIC_API_KEY not set")
    
    # Gate 2: Load V1 profile (can be mocked — not testing this)
    v1_profile = load_sample_v1_profile("albright_college")
    
    # Gate 3: Run REAL V2 enhancement (NO MOCKS)
    result = enhance_profile_with_v2_lite(
        v1_profile=v1_profile,
        university_name="Albright College",
        ein="23-1352650",
        enable_v2=True
    )
    
    # Assertions: Real API call validation
    assert result['metadata']['intelligence_queries_used'] == 3
    assert 'v2_signals' in result
    assert result['v2_signals']['composite_score'] >= 85
    assert result['v2_signals']['urgency_flag'] in ['HIGH', 'IMMEDIATE']
    
    # Print for manual review
    print("\n=== LIVE API TEST RESULTS ===")
    print(f"Composite Score: {result['v2_signals']['composite_score']}")
    print(f"Urgency: {result['v2_signals']['urgency_flag']}")
    print(f"Queries Used: {result['metadata']['intelligence_queries_used']}")
```

---

### Phase 4: Live API Validation (30 minutes)

**Objective**: Execute real Albright College test with live Perplexity API.

**Prerequisites**:
- ✅ `PERPLEXITY_API_KEY` set in environment
- ✅ `ANTHROPIC_API_KEY` set in environment
- ✅ Test mocks removed from `test_albright_smoke.py`
- ✅ `recon.py` verified to use direct API

**Execution**:
```bash
# 1. Set environment variables (if not already set)
export PERPLEXITY_API_KEY="pplx-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# 2. Run integration test with verbose output
cd agents/analyst
pytest tests/integration/test_albright_smoke.py -v -s

# 3. Expected output:
# [ANALYST] [V2] Enhancing profile with real-time intelligence...
# [RECON] Executing query 1/3: Albright College enrollment...
# [RECON] Executing query 2/3: Albright College leadership...
# [RECON] Executing query 3/3: Albright College accreditation...
# [SYNTHESIS] Extracting signals from 3 query results...
# [CLASSIFICATION] Calculating composite score...
# ✓ Composite score: 94
# ✓ Urgency: IMMEDIATE
# ✓ Queries used: 3
```

**Success Criteria**:
- ✅ Test completes without exceptions
- ✅ Console logs show "Executing query 1/3..." (real API calls)
- ✅ Composite score ≥ 85 (Albright is known distressed)
- ✅ Urgency flag = HIGH or IMMEDIATE
- ✅ Query count = exactly 3
- ✅ Processing time < 60 seconds

**Failure Scenarios & Fixes**:

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `ValueError: PERPLEXITY_API_KEY not found` | Key not set | Export env var, re-run |
| `401 Unauthorized` | Invalid API key | Get new key from dashboard |
| `429 Rate Limit` | Too many requests | Wait 60 seconds, retry |
| `ConnectionError` | Network issue | Check internet, retry |
| `Timeout` | Perplexity API slow | Increase timeout to 60s |
| Test passes but logs show no "Executing query" | Mocks still active | Remove @patch decorators |

---

## SECTION 5: DELIVERABLES & ACCEPTANCE CRITERIA

### Deliverable 1: API Connectivity Validation Report

**Format**: Markdown document  
**Location**: `tests/integration/API_CONNECTIVITY_REPORT.md`

**Required Sections**:
1. **Environment Check**: PERPLEXITY_API_KEY status (set/not set)
2. **API Test Results**: Direct API call test (200 OK or error)
3. **Recon Module Audit**: Confirmation of direct API usage (not MCP)
4. **Live Test Results**: Albright smoke test output (composite score, urgency)
5. **Timestamp**: When validation completed

**Template**:
```markdown
# API Connectivity Validation Report

**Date**: YYYY-MM-DD HH:MM  
**Engineer**: Lead Engineer  
**Status**: ✅ VALIDATED or ❌ BLOCKED

## 1. Environment Check
- PERPLEXITY_API_KEY: ✅ Set (pplx-xxxxx...)
- ANTHROPIC_API_KEY: ✅ Set (sk-ant-xxxxx...)

## 2. Direct API Test
- Endpoint: https://api.perplexity.ai/chat/completions
- Status: 200 OK
- Response time: 1.2s
- Result: ✅ API connectivity confirmed

## 3. Recon Module Audit
- File: agents/analyst/sources/v2_lite/recon.py
- API Method: requests.post (direct API)
- MCP Usage: None (bypassed)
- Result: ✅ Direct API implementation confirmed

## 4. Live Albright Test
- Composite Score: 94
- Urgency: IMMEDIATE
- Queries Used: 3
- Processing Time: 47 seconds
- Result: ✅ Real API calls successful

## 5. Gate 2 Readiness
Status: ✅ READY FOR 5-UNIVERSITY BATCH TEST
```

---

### Deliverable 2: API Setup Documentation

**Format**: Markdown user guide  
**Location**: `docs/API_SETUP_GUIDE.md`

**Purpose**: Enable future users (Aaron, other team members) to configure API access without architect support.

**Required Sections**:
1. **Prerequisites**: Where to get API keys (Perplexity dashboard, Anthropic dashboard)
2. **Environment Configuration**: How to set `PERPLEXITY_API_KEY` and `ANTHROPIC_API_KEY`
3. **Validation Steps**: How to test API connectivity before running analyst
4. **Troubleshooting**: Common errors and fixes
5. **Cost Estimates**: API usage costs per university analysis

**Template Outline**:
```markdown
# API Setup Guide: Analyst V2.0-LITE

## Step 1: Get API Keys
- Perplexity: https://www.perplexity.ai/settings/api
- Anthropic: https://console.anthropic.com/settings/keys

## Step 2: Set Environment Variables
### Option A: Terminal Session (Temporary)
```bash
export PERPLEXITY_API_KEY="pplx-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### Option B: .env File (Persistent)
Create `.env` in project root:
```
PERPLEXITY_API_KEY=pplx-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
```

## Step 3: Validate Connectivity
Run validation script:
```bash
python scripts/validate_api_keys.py
```

## Troubleshooting
- Error: "PERPLEXITY_API_KEY not found" → Set environment variable
- Error: "401 Unauthorized" → Check API key is valid
- Error: "429 Rate Limit" → Wait 60 seconds, retry
```

---

### Deliverable 3: Updated Test Suite

**Files Modified**:
- `tests/integration/test_albright_smoke.py` (remove mocks)
- `tests/integration/test_v2_resilience.py` (keep mocks — this tests failure scenarios)

**New Files**:
- `tests/integration/conftest.py` (pytest configuration for API key checks)
- `scripts/validate_api_keys.py` (standalone validation utility)

**Acceptance Criteria**:
- ✅ `test_albright_smoke.py` uses NO mocks for API calls
- ✅ Test fails fast if API keys not configured (pytest.skip)
- ✅ Test marked with `@pytest.mark.integration`
- ✅ Console output shows "Executing query X/3" logs
- ✅ Test completes in <60 seconds

---

## SECTION 6: ROLLBACK PLAN

### If Direct API Fails After 2 Hours of Debugging

**Trigger**: Unable to get Perplexity direct API working after 2 hours of effort.

**Action**: Revert to V1-only mode, block Gate 2 deployment.

**Steps**:
1. Set `enable_v2_lite: bool = False` as default in `analyst.py`
2. Document blocker in PMO status report
3. Escalate to CSO: "V2.0-LITE blocked pending API resolution"
4. Schedule architect/engineer deep-dive session (4+ hours) to debug MCP path

**Timeline Impact**:
- Gate 2 deployment: Delayed indefinitely
- 21-university backlog: Processed with V1-only (no real-time intelligence)
- Competitive advantage: Lost until V2 functional

**Strategic Fallback**:
- Continue V1-only operations (proven, stable)
- Treat V2.0-LITE as "Phase 7" enhancement (non-critical)
- Re-evaluate MCP integration strategy

---

## SECTION 7: SUCCESS CRITERIA

### Technical Validation

- ✅ `PERPLEXITY_API_KEY` set and validated
- ✅ Direct API call to Perplexity returns 200 OK
- ✅ `recon.py` confirmed to use `requests.post` (not MCP)
- ✅ Test mocks removed from `test_albright_smoke.py`
- ✅ Live Albright test produces composite score ≥ 85
- ✅ Live test uses exactly 3 Perplexity queries
- ✅ Processing time < 60 seconds

### Documentation Validation

- ✅ `API_CONNECTIVITY_REPORT.md` generated with test results
- ✅ `API_SETUP_GUIDE.md` created for future users
- ✅ Troubleshooting section covers common errors

### Gate 2 Readiness

- ✅ Real API calls validated (not mocked)
- ✅ Composite scoring produces defensible results
- ✅ CSO can review live API output (tomorrow 10am session)
- ✅ 5-university batch test ready to execute (Feb 5)

---

## SECTION 8: HANDOVER TO LEAD ENGINEER

### Your Mission (2-Hour Sprint)

**Phase 1** (30 min): Environment & API Validation
1. Check `PERPLEXITY_API_KEY` environment variable
2. Run direct API connectivity test (Python snippet in Section 4, Phase 1)
3. Document results in `API_CONNECTIVITY_REPORT.md`

**Phase 2** (30 min): Code Audit
1. Open `agents/analyst/sources/v2_lite/recon.py`
2. Confirm `_call_perplexity()` uses `requests.post` (not MCP)
3. Verify endpoint URL: `https://api.perplexity.ai/chat/completions`
4. Check error handling for network failures

**Phase 3** (30 min): Remove Test Mocks
1. Open `tests/integration/test_albright_smoke.py`
2. Remove all `@patch` decorators for API calls
3. Add API key validation (pytest.skip if missing)
4. Add `@pytest.mark.integration` decorator

**Phase 4** (30 min): Live API Test
1. Run `pytest tests/integration/test_albright_smoke.py -v -s`
2. Confirm console logs show "Executing query 1/3..."
3. Validate composite score ≥ 85, urgency = HIGH/IMMEDIATE
4. Document results in `API_CONNECTIVITY_REPORT.md`

**Deliverables**:
- [ ] `tests/integration/API_CONNECTIVITY_REPORT.md` (validation results)
- [ ] `docs/API_SETUP_GUIDE.md` (user-facing documentation)
- [ ] `tests/integration/test_albright_smoke.py` (mocks removed)
- [ ] Confirmation: "Live API test passed, Gate 2 ready"

---

### Critical Questions for Engineer

**Before You Start**:
1. Do you have access to `PERPLEXITY_API_KEY`? (Check with Aaron/PMO if not)
2. Can you run `echo $PERPLEXITY_API_KEY` and see a value starting with `pplx-`?
3. Do you have `requests` library installed? (`pip install requests`)

**During Debugging** (if API test fails):
1. What is the exact error message from Perplexity API?
2. What HTTP status code did the API return? (200? 401? 429?)
3. Does `recon.py` use `requests.post` or `mcp_client.call_tool`?

**After Validation**:
1. Did live Albright test produce composite score ≥ 85?
2. Did console logs show "Executing query 1/3..." (proof of real API)?
3. Is `API_CONNECTIVITY_REPORT.md` complete with all sections?

---

### Communication Protocol

**Immediate Escalation Triggers** (notify Architect within 15 min):
- ❌ `PERPLEXITY_API_KEY` not found and cannot locate key source
- ❌ Direct API test returns 401 Unauthorized (invalid key)
- ❌ `recon.py` code review reveals MCP integration (not direct API)
- ❌ After 1 hour, still cannot get live API call to succeed

**Hourly Status Updates** (Slack #operation-sniper):
- After 30 min: Phase 1 complete (environment validated)
- After 1 hour: Phase 2-3 complete (code audited, mocks removed)
- After 1.5 hours: Phase 4 in progress (live test running)
- After 2 hours: DONE or ESCALATE

**Success Notification** (Slack + PMO):
```
✅ API CONNECTIVITY VALIDATED
- Live Albright test: PASS (score 94, IMMEDIATE urgency)
- Real API calls confirmed (3 Perplexity queries)
- Gate 2 ready: 5-university batch can proceed
- Deliverables: API_CONNECTIVITY_REPORT.md, API_SETUP_GUIDE.md
```

---

## SECTION 9: ARCHITECT'S NOTES

### Why This Blueprint is Different

This is a **debugging blueprint**, not a feature build. Key differences:

1. **Validation-First**: We're not writing new code—we're validating existing code works with real APIs
2. **Fast Iteration**: 2-hour sprint (not 6-hour implementation)
3. **Binary Outcome**: Either API works (Gate 2 proceeds) or it doesn't (block deployment)
4. **Minimal Changes**: Remove mocks, validate connectivity—no refactoring

### What We're NOT Doing

- ❌ Building new MCP integration
- ❌ Refactoring recon.py architecture
- ❌ Adding new features or capabilities
- ❌ Optimizing query performance
- ❌ Implementing caching or rate limiting

**Focus**: Prove the system works with real APIs. That's it.

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API key not available | Low | Critical | Escalate to Aaron immediately |
| Perplexity API down | Very Low | High | Retry after 1 hour |
| Code uses MCP (not direct API) | Medium | High | 2-hour rollback window in place |
| Test still uses mocks | Low | Medium | Code review in Phase 3 |
| Rate limit hit during test | Low | Low | Wait 60s, retry |

**Overall Risk**: **MEDIUM** (but manageable with 2-hour time box)

---

### Success Definition

**Minimum Viable Success**:
- Live Albright test completes without exceptions
- Console logs prove real API calls made (not mocks)
- Composite score is reasonable (≥ 75)

**Full Success**:
- Live Albright test produces score ≥ 85, urgency IMMEDIATE
- All 3 Perplexity queries execute successfully
- Documentation complete for future users
- CSO can review live output tomorrow (10am)

**If We Fail**:
- V1-only mode becomes default
- V2.0-LITE becomes "Phase 7" (non-critical enhancement)
- Gate 2 deployment blocked indefinitely

**Stakes**: This 2-hour sprint determines whether V2.0-LITE launches Feb 6 or gets shelved for weeks.

---

## SECTION 10: AUTHORIZATION

**Approved By**: Chief Systems Architect  
**Authorization Date**: February 3, 2026  
**Sprint Duration**: 2 hours (time-boxed)  
**Priority**: **P0 — PRODUCTION BLOCKER**

**Approved Actions**:
1. Validate Perplexity API connectivity (direct API, not MCP)
2. Remove test mocks from `test_albright_smoke.py`
3. Execute live Albright College API test
4. Document results in `API_CONNECTIVITY_REPORT.md`
5. Create `API_SETUP_GUIDE.md` for future users

**Rollback Trigger**: If after 2 hours API connectivity not validated, escalate to Architect for MCP deep-dive session (4+ hours).

**Next Gate**: If validation succeeds, proceed to Gate 2 (5-university batch test, Feb 5).

---

**END TECHNICAL BLUEPRINT**

---

**Handover to Lead Engineer approved. Begin Phase 6.5 API Debug Sprint.**

**Expected Completion**: February 3, 2026, 11:59 PM (2-hour sprint from now)

**Success Signal**: "✅ API CONNECTIVITY VALIDATED — GATE 2 READY"