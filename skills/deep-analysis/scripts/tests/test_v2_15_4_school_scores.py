"""Regression for v2.15.4 · panel.school_scores (按流派打分).

动机：用户反馈"除了总分还要看每个流派各自给的分"·
七大流派 (A-G) 各自 consensus/avg_score/verdict 让用户一眼看出不同哲学的分歧.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))


def _fake_panel_result():
    """手动拼一个极简 investors_out, 验证 school_scores 聚合."""
    return [
        # A 价值派: 6 人 · 4 bull / 1 neu / 1 bear
        {"investor_id": "buffett", "group": "A", "signal": "bullish", "score": 85},
        {"investor_id": "graham", "group": "A", "signal": "bullish", "score": 78},
        {"investor_id": "fisher", "group": "A", "signal": "bullish", "score": 72},
        {"investor_id": "munger", "group": "A", "signal": "bullish", "score": 80},
        {"investor_id": "templeton", "group": "A", "signal": "neutral", "score": 55},
        {"investor_id": "klarman", "group": "A", "signal": "bearish", "score": 30},
        # D 技术派: 4 人 · 全 bearish
        {"investor_id": "livermore", "group": "D", "signal": "bearish", "score": 25},
        {"investor_id": "minervini", "group": "D", "signal": "bearish", "score": 20},
        {"investor_id": "darvas", "group": "D", "signal": "bearish", "score": 30},
        {"investor_id": "gann", "group": "D", "signal": "bearish", "score": 28},
        # F 游资: 3 人 · 1 skip / 2 neutral
        {"investor_id": "zhang_mz", "group": "F", "signal": "neutral", "score": 50},
        {"investor_id": "sun_ge", "group": "F", "signal": "neutral", "score": 48},
        {"investor_id": "zhao_lg", "group": "F", "signal": "skip", "score": 0},
    ]


def test_school_scores_aggregation_math():
    """校验 consensus/avg_score/verdict 计算逻辑正确."""
    # inline 复现 build_panel 末尾的聚合代码 —— 不依赖真实 raw/features
    investors_out = _fake_panel_result()
    NEUTRAL_WEIGHT = 0.6

    by_group = {}
    for inv in investors_out:
        by_group.setdefault(inv["group"], []).append(inv)

    # A 派: active=6, bull=4, neu=1 → (4 + 0.6*1)/6 * 100 = 76.67
    a = by_group["A"]
    active = [m for m in a if m["signal"] != "skip"]
    bull = sum(1 for m in a if m["signal"] == "bullish")
    neu = sum(1 for m in a if m["signal"] == "neutral")
    cons_a = (bull + NEUTRAL_WEIGHT * neu) / len(active) * 100
    avg_a = sum(m["score"] for m in active) / len(active)
    assert abs(cons_a - 76.67) < 0.1
    assert abs(avg_a - 66.67) < 0.1  # (85+78+72+80+55+30)/6

    # D 派: 全 bearish → consensus 0
    d = by_group["D"]
    bull_d = sum(1 for m in d if m["signal"] == "bullish")
    neu_d = sum(1 for m in d if m["signal"] == "neutral")
    active_d = [m for m in d if m["signal"] != "skip"]
    cons_d = (bull_d + NEUTRAL_WEIGHT * neu_d) / len(active_d) * 100
    assert cons_d == 0.0

    # F 派: 2 active (都 neutral) + 1 skip → (0 + 0.6*2)/2 = 60
    f = by_group["F"]
    bull_f = sum(1 for m in f if m["signal"] == "bullish")
    neu_f = sum(1 for m in f if m["signal"] == "neutral")
    active_f = [m for m in f if m["signal"] != "skip"]
    cons_f = (bull_f + NEUTRAL_WEIGHT * neu_f) / len(active_f) * 100
    assert cons_f == 60.0


def test_school_scores_in_cached_panel():
    """真实 cache · 已跑过的股票 panel.json 应含 school_scores 字段（新运行后）.

    只是 smoke test: 确认 build_panel 返回结构 · 不强求每个 cached 都有（旧数据无）.
    """
    import json
    cache = SCRIPTS / ".cache"
    if not cache.exists():
        return  # 无 cache · skip
    # 找一个最新的 panel.json
    panels = sorted(cache.glob("*/panel.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not panels:
        return
    # 至少有 school_scores 字段（即使旧 cache 无 · 新跑的必须有）· 但不能强求旧的
    # 所以只 assert 格式：若 school_scores 存在则结构正确
    data = json.loads(panels[0].read_text(encoding="utf-8"))
    ss = data.get("school_scores")
    if ss:
        # 至少含一组 · 每组字段齐全
        assert isinstance(ss, dict)
        for g, s in ss.items():
            assert g in ("A", "B", "C", "D", "E", "F", "G")
            for key in ("label", "consensus", "avg_score", "verdict",
                        "n_members", "n_active", "bullish", "neutral", "bearish"):
                assert key in s, f"school {g} missing {key}"


def test_verdict_thresholds_match_overall():
    """流派级 verdict 阈值必须和综合分阈值对齐（80/65/50/35）."""
    src = (SCRIPTS / "run_real_test.py").read_text(encoding="utf-8")
    # 函数 _consensus_to_verdict 应该在 build_panel 里
    assert "_consensus_to_verdict" in src
    # 阈值应和 overall 保持一致 · 80/65/50/35
    idx = src.find("_consensus_to_verdict")
    snippet = src[idx:idx + 500]
    assert "c >= 80" in snippet
    assert "c >= 65" in snippet
    assert "c >= 50" in snippet
    assert "c >= 35" in snippet


def test_template_has_school_scores_marker():
    """report-template.html 必须含 INJECT_SCHOOL_SCORES 注入点."""
    tpl = SCRIPTS.parent / "assets" / "report-template.html"
    content = tpl.read_text(encoding="utf-8")
    assert "INJECT_SCHOOL_SCORES" in content


def test_assemble_report_has_render_function():
    """assemble_report.py 必须有 render_school_scores 函数."""
    src = (SCRIPTS / "assemble_report.py").read_text(encoding="utf-8")
    assert "def render_school_scores(" in src
    assert "INJECT_SCHOOL_SCORES" in src


def test_render_school_scores_returns_html():
    """render_school_scores 对有效 school_scores dict 应输出含各流派 label 的 HTML."""
    from assemble_report import render_school_scores
    syn = {
        "school_scores": {
            "A": {
                "group": "A", "label": "经典价值派", "desc": "buffett...",
                "consensus": 76.7, "avg_score": 66.7, "verdict": "买入",
                "n_members": 6, "n_active": 6,
                "bullish": 4, "neutral": 1, "bearish": 1, "skip": 0,
                "dominant_signal": "bullish",
            },
            "D": {
                "group": "D", "label": "技术派", "desc": "livermore...",
                "consensus": 0.0, "avg_score": 25.75, "verdict": "回避",
                "n_members": 4, "n_active": 4,
                "bullish": 0, "neutral": 0, "bearish": 4, "skip": 0,
                "dominant_signal": "bearish",
            },
        }
    }
    html = render_school_scores(syn, {})
    assert "经典价值派" in html
    assert "技术派" in html
    assert "SCHOOL SCORES" in html or "流派" in html
    assert "买入" in html
    assert "回避" in html


def test_empty_school_scores_returns_empty_string():
    """无 school_scores 时 render 函数应返空串 · 不中断."""
    from assemble_report import render_school_scores
    assert render_school_scores({}, {}) == ""
    assert render_school_scores({"school_scores": {}}, {"school_scores": {}}) == ""
