# ANALYST V2.0-LITE QUICK REFERENCE

## Implementation Complete ✅

All files for Phase 5 implementation have been created and validated.

---

## Files Created (7 total)

### New Modules (5)
1. ✅ `agents/analyst/sources/v2_lite/__init__.py` - Package initialization
2. ✅ `agents/analyst/sources/v2_lite/recon.py` - Perplexity 3-query client
3. ✅ `agents/analyst/sources/v2_lite/synthesis.py` - Claude signal extraction
4. ✅ `agents/analyst/sources/v2_lite/classification.py` - V1+V2 scoring
5. ✅ `agents/analyst/core/orchestrator.py` - Master pipeline orchestrator

### Configuration & Schema (2)
6. ✅ `agents/analyst/config/prompts/synthesis_v2.txt` - System prompt
7. ✅ `shared/schemas/prospect_profile_schema.json` - JSON Schema v2.0.0

---

## Architecture Overview

```
INPUT (from V1 Pipeline)
    ↓
    └─→ [Phase 5a: Reconnaissance]
        └─→ 3 Perplexity queries (enrollment, leadership, accreditation)
    ↓
    └─→ [Phase 5b: Signal Extraction]
        └─→ Claude extracts structured signals + citations
    ↓
    └─→ [Phase 6: Composite Scoring]
        └─→ V1 base + V2 amplification (TRUSTED signals only)
    ↓
OUTPUT (Enhanced Profile v2.0.0)
    └─→ Backward compatible with V1 systems
```

---

## Key Features

### 🎯 Scope Adherence
- ✅ Exactly 3 queries (no more, no less)
- ✅ Binary credibility (TRUSTED/UNTRUSTED only)
- ✅ Citation discipline (source + date mandatory)
- ✅ No weighted scoring (gates based on credibility)

### 🔒 Constraints Enforced
- Query budget: Hard-coded limit of 3 per university
- Score range: Always 0-100 (min/max enforced)
- Compositing: Only TRUSTED signals amplify score
- Backward compatibility: V2 block is optional

### 📊 Scoring Logic
| Signal | V2 Contribution | When Counted |
|--------|-----------------|--------------|
| Enrollment decline | +10 | Source = TRUSTED |
| Leadership change | +15 | Source = TRUSTED |
| Accreditation warning | +20 | Source = TRUSTED |
| **Max amplification** | **+45** | All signals triggered |

**Urgency Mapping**:
- `IMMEDIATE`: score ≥ 90 (crisis intervention)
- `HIGH`: score 75-89 (active engagement)
- `MONITOR`: score < 75 (watch for escalation)

---

## Usage Examples

### Basic Reconnaissance
```python
from agents.analyst.sources.v2_lite import execute_recon

results = execute_recon(
    university_name="Albright College",
    ein="23-1352650"
)
# 3 Perplexity queries executed, raw results returned
```

### Signal Extraction
```python
from agents.analyst.sources.v2_lite import extract_signals

signals = extract_signals(
    raw_perplexity_results=results['raw_results'],
    university_name="Albright College"
)
# Claude extracts structured signals with citations
```

### Composite Scoring
```python
from agents.analyst.sources.v2_lite.classification import calculate_composite_score

score = calculate_composite_score(
    v1_signals={'pain_level': 85},
    v2_signals=signals['signals']
)
# Returns composite_score (0-100) + urgency_flag
```

### Full Pipeline
```python
from agents.analyst.core import enhance_profile_with_v2_lite

enhanced = enhance_profile_with_v2_lite(
    v1_profile=original_profile,
    university_name="Albright College",
    ein="23-1352650",
    enable_v2=True
)
# Orchestrates Phases 5-6, returns enhanced profile
```

---

## Integration into analyst.py

Add this to `agents/analyst/analyst.py` in the `generate_dossier()` function, after building the V1 profile:

```python
# After: profile = build_profile_json(...)
# Add:

if enable_v2_lite:  # Add param to function signature
    print("[ANALYST] [V2] Starting real-time intelligence phase...")
    from agents.analyst.core import enhance_profile_with_v2_lite
    
    profile = enhance_profile_with_v2_lite(
        v1_profile=profile,
        university_name=target_name,
        ein=ein,
        enable_v2=True
    )
    
    v2_data = profile.get('v2_signals', {})
    print(f"[ANALYST] [V2] ✓ Enhanced with composite score: {v2_data.get('composite_score')}")
    print(f"[ANALYST] [V2] ✓ Urgency flag: {v2_data.get('urgency_flag')}")
```

---

## Environment Variables Required

```bash
# .env file
PERPLEXITY_API_KEY=your_perplexity_key
ANTHROPIC_API_KEY=your_anthropic_key
```

---

## Dependencies to Install

```bash
pip install anthropic>=0.25.0
pip install requests>=2.31.0
```

---

## Validation Checklist

### File Existence
- [x] All 5 Python modules created
- [x] System prompt file created
- [x] Schema file created
- [x] Core orchestrator created

### Code Quality
- [x] No syntax errors (verified via imports)
- [x] Docstrings present and comprehensive
- [x] Type hints included
- [x] Error handling implemented

### Specification Compliance
- [x] 3-query budget enforced
- [x] Binary credibility classification
- [x] Citation discipline
- [x] Backward compatibility
- [x] Composite scoring logic
- [x] Urgency flags (IMMEDIATE/HIGH/MONITOR)

### Schema Validation
- [x] JSON is valid
- [x] Version 2.0.0 correct
- [x] v2_signals block optional
- [x] Definitions complete

---

## Next Steps for Lead Engineer

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export PERPLEXITY_API_KEY=...
   export ANTHROPIC_API_KEY=...
   ```

3. **Integrate with analyst.py**
   - Add import statement
   - Add V2-LITE enhancement call
   - Test with flag toggled on/off

4. **Run Integration Test**
   ```bash
   python3 agents/analyst/analyst.py \
     --target "Albright College" \
     --ein "23-1352650"
   ```

5. **Validate Output**
   - Check JSON validates against schema v2.0.0
   - Verify v2_signals block present
   - Confirm composite_score in range 0-100
   - Check urgency_flag is IMMEDIATE/HIGH/MONITOR

6. **Deploy Staging**
   - Test with full prospect list
   - Monitor Perplexity/Claude API usage
   - Validate error handling

7. **Production Deployment**
   - Aaron CSO approval
   - Merge to main branch
   - Monitor in production

---

## Support & Questions

**Technical Issues**: Review TECHNICAL BLUEPRINT attached file

**API Key Setup**: See `.env.example` in project root

**Schema Validation**: Use `jsonschema` library:
```python
from jsonschema import validate
import json

with open('shared/schemas/prospect_profile_schema.json') as f:
    schema = json.load(f)
validate(instance=profile, schema=schema)
```

---

**Status**: ✅ COMPLETE & READY FOR INTEGRATION  
**Version**: 2.0.0-LITE  
**Date**: February 3, 2026
