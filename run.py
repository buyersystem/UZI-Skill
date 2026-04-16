#!/usr/bin/env python3
"""UZI-Skill 一键运行入口 — 适用于 Codex / 命令行 / 任何 agent。

用法:
    python run.py 002273.SZ          # A 股
    python run.py 600519.SH          # A 股
    python run.py 00700.HK           # 港股
    python run.py AAPL               # 美股
    python run.py 贵州茅台            # 中文名也行

跑完后自动打开浏览器展示 HTML 报告。
"""
import os
import sys

# 确保编码正确
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# 把 scripts 目录加到 path
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "skills", "deep-analysis", "scripts")
sys.path.insert(0, SCRIPTS_DIR)
os.chdir(SCRIPTS_DIR)

from run_real_test import main

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "002273.SZ"
    print(f"\n🎯 UZI-Skill v2.0 · 游资 Skills · 深度分析")
    print(f"   目标: {ticker}")
    print(f"   数据目录: {SCRIPTS_DIR}")
    print()
    main(ticker)
