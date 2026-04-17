"""网络预检 · v2.10.2.

在 stage1 开始前快速 ping 几个关键域名，如果代理/GFW 挂了，**立即**告诉
用户，而不是让他等 10 分钟每个 fetcher 挨个超时。

**检查目标**:
  · push2.eastmoney.com      — akshare 行情主源
  · duckduckgo.com            — ddgs web search
  · api.github.com            — 通用 canary (理论上不会被墙但代理可能挂)

**输出**: 3 个域名的可达性 + 总体建议

**使用**:
    from lib.network_preflight import run_preflight
    result = run_preflight()
    if result["critical_failures"] > 2:
        print("⚠️ 代理似乎大面积不通，建议 --depth lite 或修代理")
"""
from __future__ import annotations

import socket
import time
from dataclasses import dataclass


@dataclass
class DomainCheck:
    domain: str
    reachable: bool
    latency_ms: int
    error: str = ""
    purpose: str = ""


_TARGETS = [
    ("push2.eastmoney.com", "A 股行情 (akshare 主源)"),
    ("duckduckgo.com",       "ddgs 定性查询"),
    ("www.cninfo.com.cn",    "cninfo 行业 PE + 公告"),
    ("stock.xueqiu.com",     "雪球数据"),
    ("api.github.com",       "通用网络健康度"),
]


def _probe(domain: str, port: int = 443, timeout: float = 3.0) -> DomainCheck:
    """TCP connect probe（不做 HTTP，只测底层连通）."""
    t0 = time.time()
    try:
        sock = socket.create_connection((domain, port), timeout=timeout)
        sock.close()
        return DomainCheck(
            domain=domain,
            reachable=True,
            latency_ms=int((time.time() - t0) * 1000),
        )
    except socket.gaierror as e:
        return DomainCheck(domain=domain, reachable=False, latency_ms=int((time.time() - t0) * 1000),
                           error=f"DNS fail: {e}")
    except socket.timeout:
        return DomainCheck(domain=domain, reachable=False, latency_ms=int(timeout * 1000),
                           error=f"timeout > {timeout}s")
    except Exception as e:
        return DomainCheck(domain=domain, reachable=False, latency_ms=int((time.time() - t0) * 1000),
                           error=f"{type(e).__name__}: {str(e)[:80]}")


def run_preflight(verbose: bool = True, timeout: float = 3.0) -> dict:
    """跑一遍预检。返回诊断字典."""
    results: list[DomainCheck] = []
    for domain, purpose in _TARGETS:
        r = _probe(domain, timeout=timeout)
        r.purpose = purpose
        results.append(r)

    reachable = sum(1 for r in results if r.reachable)
    failures = len(results) - reachable
    avg_latency = sum(r.latency_ms for r in results if r.reachable) / max(reachable, 1)

    # 决策
    if failures == 0:
        advisory = "✓ 网络畅通"
        severity = "ok"
    elif failures == 1:
        advisory = "⚠ 单点不通，整体可跑（可能个别 fetcher 降级）"
        severity = "warning"
    elif failures == 2:
        advisory = "⚠⚠ 多点不通，建议 --depth lite 节省时间"
        severity = "degraded"
    else:
        advisory = "🔴 代理/网络严重不通，强烈建议先修网络或用 --depth lite"
        severity = "critical"

    if verbose:
        print(f"\n🌐 网络预检 ({reachable}/{len(results)} 通 · 均延迟 {avg_latency:.0f}ms)")
        for r in results:
            mark = f"✓ {r.latency_ms:4d}ms" if r.reachable else f"✗ {r.error[:40]}"
            print(f"  {mark}  {r.domain:28} · {r.purpose}")
        print(f"\n  {advisory}\n")

    return {
        "reachable": reachable,
        "failures": failures,
        "critical_failures": failures,  # alias
        "avg_latency_ms": int(avg_latency),
        "advisory": advisory,
        "severity": severity,
        "results": [
            {"domain": r.domain, "reachable": r.reachable, "latency_ms": r.latency_ms,
             "error": r.error, "purpose": r.purpose}
            for r in results
        ],
    }


if __name__ == "__main__":
    run_preflight(verbose=True)
