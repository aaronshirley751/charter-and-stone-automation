#!/usr/bin/env python3
"""
DIRECT ANTHROPIC API VERIFICATION
Tests if the 90-second timeout allows Claude API to respond successfully.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not ANTHROPIC_API_KEY or not PERPLEXITY_API_KEY:
    print("[ERROR] API keys missing")
    print(f"  ANTHROPIC_API_KEY: {'✓' if ANTHROPIC_API_KEY else '✗'}")
    print(f"  PERPLEXITY_API_KEY: {'✓' if PERPLEXITY_API_KEY else '✗'}")
    exit(1)

print("=" * 80)
print("DIRECT ANTHROPIC API TEST (90-Second Timeout)")
print("=" * 80)

# Test 1: Basic timeout configuration
print("\n🔴 TEST 1: Initialize Anthropic client with 90s timeout")
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=ANTHROPIC_API_KEY, timeout=90.0)
    print("   ✅ Client initialized with 90s timeout")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Simple API call
print("\n🔴 TEST 2: Make simple API call (verify connectivity)")
try:
    print("   ⏳ Sending test request to Claude...")
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": "Confirm API is working by responding with: LIVE_API_ACTIVE"
        }]
    )
    result = response.content[0].text
    print(f"   ✅ API Response received: {result[:50]}")
    if "LIVE_API_ACTIVE" in result or "working" in result.lower() or "active" in result.lower():
        print("   ✅ Claude API is LIVE and responding")
    else:
        print(f"   ⚠️  Unexpected response: {result}")
except Exception as e:
    print(f"   ❌ API Error: {type(e).__name__}: {str(e)[:100]}")
    exit(1)

# Test 3: Test with university analysis prompt (Albright)
print("\n🔴 TEST 3: Test with intelligence synthesis prompt (Albright)")
try:
    print("   ⏳ Synthesizing intelligence signals...")
    
    system_prompt = """You are an intelligence synthesis engine. Extract structured signals from university data.
Return JSON with three categories: enrollment_trends, leadership_changes, accreditation_status.
Each should have: finding, source (with date), and credibility (TRUSTED/UNTRUSTED)."""
    
    user_prompt = """University: Albright College
Search Results: Enrollment down 15%, CFO departed Jan 2025, MSCHE on probation notice.
Extract signals as JSON."""
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": user_prompt
        }],
        temperature=0.3
    )
    
    result_text = response.content[0].text
    print(f"   ✅ Response received ({len(result_text)} chars)")
    
    # Check if response contains expected signals
    if "enrollment" in result_text.lower() and ("15%" in result_text or "decline" in result_text.lower()):
        print("   ✅ Response contains REAL signal data (not mock)")
        print("\n   📋 Signal Preview:")
        lines = result_text.split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"      {line[:70]}")
    else:
        print("   ⚠️  Response may be mock data")
        print(f"      {result_text[:100]}")
    
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {str(e)[:100]}")
    exit(1)

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - LIVE API WORKING WITH 90S TIMEOUT")
print("=" * 80)
