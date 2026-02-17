#!/usr/bin/env python3
"""
Kisan-Eye V6 — Stress Test
Hammers all API endpoints with concurrent requests.
Measures latencies (P50/P95/P99), throughput, and error rates.

Usage:  python stress_test.py
"""

import asyncio
import time
import json
import statistics
import sys
from dataclasses import dataclass, field
from typing import Optional

try:
    import aiohttp
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp

BASE_URL = "http://localhost:8000"

# ── Test Configuration ──
CONCURRENT_USERS = 10       # Simultaneous requests
ROUNDS = 3                  # How many rounds per endpoint
LLM_CONCURRENT = 2          # LLM is slow — use fewer concurrent
LLM_ROUNDS = 1

@dataclass
class EndpointResult:
    name: str
    latencies: list = field(default_factory=list)
    errors: int = 0
    status_codes: dict = field(default_factory=dict)

    @property
    def success_count(self):
        return len(self.latencies)

    @property
    def total(self):
        return self.success_count + self.errors

    @property
    def p50(self):
        return self._percentile(50)

    @property
    def p95(self):
        return self._percentile(95)

    @property
    def p99(self):
        return self._percentile(99)

    @property
    def avg(self):
        return statistics.mean(self.latencies) if self.latencies else 0

    @property
    def throughput(self):
        total_time = sum(self.latencies) if self.latencies else 1
        return len(self.latencies) / (total_time / len(self.latencies)) if self.latencies else 0

    def _percentile(self, p):
        if not self.latencies:
            return 0
        sorted_lat = sorted(self.latencies)
        idx = int(len(sorted_lat) * p / 100)
        return sorted_lat[min(idx, len(sorted_lat) - 1)]


async def timed_request(session, method, url, result: EndpointResult, **kwargs):
    """Make a request and record timing."""
    start = time.perf_counter()
    try:
        async with session.request(method, url, timeout=aiohttp.ClientTimeout(total=180), **kwargs) as resp:
            await resp.read()
            elapsed = time.perf_counter() - start
            result.latencies.append(elapsed)
            code = resp.status
            result.status_codes[code] = result.status_codes.get(code, 0) + 1
    except Exception as e:
        elapsed = time.perf_counter() - start
        result.errors += 1
        result.status_codes["ERR"] = result.status_codes.get("ERR", 0) + 1


async def run_test(name, coro_factory, concurrent, rounds):
    """Run a stress test for one endpoint."""
    result = EndpointResult(name=name)
    print(f"\n{'='*60}")
    print(f"  🔥 {name}")
    print(f"     {concurrent} concurrent × {rounds} rounds = {concurrent * rounds} requests")
    print(f"{'='*60}")

    start = time.perf_counter()
    for r in range(rounds):
        tasks = [coro_factory(result) for _ in range(concurrent)]
        await asyncio.gather(*tasks)
        print(f"     Round {r+1}/{rounds} done — {result.success_count} ok, {result.errors} err")

    wall_time = time.perf_counter() - start
    rps = result.total / wall_time if wall_time > 0 else 0

    print(f"\n  📊 Results:")
    print(f"     Total:     {result.total} requests in {wall_time:.1f}s")
    print(f"     Success:   {result.success_count} | Errors: {result.errors}")
    print(f"     Throughput: {rps:.1f} req/s")
    if result.latencies:
        print(f"     Avg:  {result.avg*1000:.0f}ms")
        print(f"     P50:  {result.p50*1000:.0f}ms")
        print(f"     P95:  {result.p95*1000:.0f}ms")
        print(f"     P99:  {result.p99*1000:.0f}ms")
        print(f"     Min:  {min(result.latencies)*1000:.0f}ms | Max: {max(result.latencies)*1000:.0f}ms")
    print(f"     Status: {result.status_codes}")

    return result


async def main():
    print("\n" + "🛰️ "*20)
    print("  KISAN-EYE V6 — STRESS TEST")
    print("  Target: " + BASE_URL)
    print("🛰️ "*20)

    # Quick health check first
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/health", timeout=aiohttp.ClientTimeout(total=15)) as resp:
                health = await resp.json()
                print(f"\n  ✅ Server healthy: face={health.get('face_engine')}, "
                      f"whisper={health.get('whisper')}, ollama={health.get('ollama', {}).get('available')}")
        except Exception as e:
            print(f"\n  ❌ Server not responding: {e}")
            print("     Start the backend: cd backend && python server.py")
            return

    results = []

    # ── 1. Health Check (lightweight) ──
    async with aiohttp.ClientSession() as session:
        async def health_req(r):
            await timed_request(session, "GET", f"{BASE_URL}/health", r)

        res = await run_test("GET /health", health_req, CONCURRENT_USERS, ROUNDS)
        results.append(res)

    # ── 2. Root endpoint ──
    async with aiohttp.ClientSession() as session:
        async def root_req(r):
            await timed_request(session, "GET", f"{BASE_URL}/", r)

        res = await run_test("GET /", root_req, CONCURRENT_USERS, ROUNDS)
        results.append(res)

    # ── 3. Farmer profile lookup ──
    async with aiohttp.ClientSession() as session:
        async def farmer_req(r):
            await timed_request(session, "GET", f"{BASE_URL}/farmer/1", r)

        res = await run_test("GET /farmer/1", farmer_req, CONCURRENT_USERS, ROUNDS)
        results.append(res)

    # ── 4. Scheme matching ──
    async with aiohttp.ClientSession() as session:
        async def scheme_req(r):
            await timed_request(session, "GET", f"{BASE_URL}/schemes/1", r)

        res = await run_test("GET /schemes/1", scheme_req, CONCURRENT_USERS, ROUNDS)
        results.append(res)

    # ── 5. Farm data (satellite API calls) ──
    async with aiohttp.ClientSession() as session:
        async def farm_req(r):
            await timed_request(session, "GET", f"{BASE_URL}/farm-data/1", r)

        res = await run_test("GET /farm-data/1 (satellite)", farm_req, 5, 2)  # fewer — external APIs
        results.append(res)

    # ── 6. LLM Chat (heavy — GPU inference) ──
    queries = [
        "What crops should I grow this season?",
        "How do I apply for PM-KISAN scheme?",
        "Is it going to rain this week?",
        "My rice crop has yellow spots, what should I do?",
        "Tell me about crop insurance",
    ]

    async with aiohttp.ClientSession() as session:
        query_idx = [0]
        async def chat_req(r):
            q = queries[query_idx[0] % len(queries)]
            query_idx[0] += 1
            body = json.dumps({"farmer_id": 1, "query": q, "language": "en", "mode": "text"})
            await timed_request(session, "POST", f"{BASE_URL}/chat", r,
                              data=body, headers={"Content-Type": "application/json"})

        res = await run_test("POST /chat (LLM inference)", chat_req, LLM_CONCURRENT, LLM_ROUNDS)
        results.append(res)

    # ── 7. Farmers list ──
    async with aiohttp.ClientSession() as session:
        async def list_req(r):
            await timed_request(session, "GET", f"{BASE_URL}/farmers", r)

        res = await run_test("GET /farmers", list_req, CONCURRENT_USERS, ROUNDS)
        results.append(res)

    # ══════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════
    print("\n\n" + "═"*70)
    print("  📋 STRESS TEST SUMMARY")
    print("═"*70)
    print(f"  {'Endpoint':<35} {'Total':>6} {'Err':>4} {'Avg':>8} {'P50':>8} {'P95':>8} {'P99':>8}")
    print(f"  {'─'*35} {'─'*6} {'─'*4} {'─'*8} {'─'*8} {'─'*8} {'─'*8}")

    total_requests = 0
    total_errors = 0
    all_latencies = []

    for r in results:
        total_requests += r.total
        total_errors += r.errors
        all_latencies.extend(r.latencies)

        avg_ms = f"{r.avg*1000:.0f}ms" if r.latencies else "N/A"
        p50_ms = f"{r.p50*1000:.0f}ms" if r.latencies else "N/A"
        p95_ms = f"{r.p95*1000:.0f}ms" if r.latencies else "N/A"
        p99_ms = f"{r.p99*1000:.0f}ms" if r.latencies else "N/A"

        status = "✅" if r.errors == 0 else "⚠️" if r.errors < r.total else "❌"
        print(f"  {status} {r.name:<33} {r.total:>6} {r.errors:>4} {avg_ms:>8} {p50_ms:>8} {p95_ms:>8} {p99_ms:>8}")

    print(f"  {'─'*35} {'─'*6} {'─'*4} {'─'*8} {'─'*8} {'─'*8} {'─'*8}")
    print(f"  {'TOTAL':<35} {total_requests:>6} {total_errors:>4}")

    if all_latencies:
        sorted_all = sorted(all_latencies)
        print(f"\n  🏆 Overall Stats:")
        print(f"     Total requests:  {total_requests}")
        print(f"     Total errors:    {total_errors} ({total_errors/total_requests*100:.1f}%)")
        print(f"     Global P50:      {sorted_all[len(sorted_all)//2]*1000:.0f}ms")
        print(f"     Global P95:      {sorted_all[int(len(sorted_all)*0.95)]*1000:.0f}ms")
        print(f"     Fastest:         {sorted_all[0]*1000:.0f}ms")
        print(f"     Slowest:         {sorted_all[-1]*1000:.0f}ms")

    # Grade
    fast_endpoints = sum(1 for r in results if r.p95 < 1.0 and r.errors == 0)
    grade = "A+" if fast_endpoints == len(results) else \
            "A" if fast_endpoints >= len(results) - 1 else \
            "B" if fast_endpoints >= len(results) - 2 else \
            "C" if total_errors < total_requests * 0.1 else "F"

    print(f"\n  📊 Grade: {grade}")
    print(f"     ({fast_endpoints}/{len(results)} endpoints under 1s P95 with 0 errors)")
    print("═"*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
