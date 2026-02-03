# API Setup Guide: Analyst V2.0-LITE

**Date:** 2026-02-03  
**Scope:** Perplexity + Anthropic API configuration for live V2.0-LITE execution

---

## 1) Prerequisites

- **Perplexity API key** (prefix `pplx-`)
- **Anthropic API key** (prefix `sk-ant-`)
- Python environment with `requests`, `python-dotenv`, `anthropic`

---

## 2) Environment Configuration

### Option A: One-time terminal session

```bash
export PERPLEXITY_API_KEY="pplx-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"
```

### Option B: Persistent `.env` file

Create `.env` in repository root:

```
PERPLEXITY_API_KEY=pplx-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
```

---

## 3) Connectivity Check (Direct API)

### Perplexity

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("PERPLEXITY_API_KEY")

resp = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "sonar",
        "messages": [{"role": "user", "content": "test"}]
    },
    timeout=30
)

print(resp.status_code, resp.text)
```

### Anthropic

```python
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"), timeout=90.0)

msg = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=100,
    messages=[{"role": "user", "content": "test"}]
)

print(msg.content)
```

---

## 4) Live Integration Test

Run the live integration smoke test (no mocks):

```bash
pytest tests/integration/test_albright_smoke.py -v -s
```

**Expected:**
- Execution time > 20s (network latency)
- Queries used = 3
- Composite score ≥ 85
- Urgency flag = `HIGH` or `IMMEDIATE`

---

## 5) Troubleshooting

| Error | Likely Cause | Fix |
|------|--------------|-----|
| `PERPLEXITY_API_KEY not set` | Missing env var | Export key or add `.env` |
| `401 Unauthorized` | Invalid/expired key | Rotate key in Perplexity console |
| `429 Too Many Requests` | Rate limit | Wait 60s and retry |
| `Timeout` | Slow API/network | Increase timeout or retry |
| `Model not found` | Model entitlement | Switch to `sonar` or confirm access |

---

## 6) Cost Considerations

Perplexity: 3 queries per university per run  
Anthropic: 1 synthesis call per university per run  
Track costs in vendor dashboards if batch processing.
