<div align="center">

# 游资（UZI）Skills

*"51 legendary investors review your stock picks — Buffett and a Chinese day-trader finally sit at the same table."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.com/product/claude-code)
[![Dimensions](https://img.shields.io/badge/Dimensions-22-brightgreen)]()
[![Investors](https://img.shields.io/badge/Investors-51-orange)]()
[![Methods](https://img.shields.io/badge/Institutional%20Methods-17-red)]()

China A-Share / HK / US Stock Deep Analysis Engine

[Install](#install) · [Usage](#usage) · [Jury Panel](#-51-investor-jury) · [Methods](#-17-institutional-methods) · [Screenshots](#-what-the-report-looks-like) · [FAQ](#-faq)

**English** | [中文](README.md)

</div>

---
## Thanks
Linux.do is all your need to learn AI~
thansk [Linux.do](https://linux.do/) for support
## What Is This

One sentence: enter a stock ticker, Claude becomes your personal analyst — pulls 22 dimensions of data, runs 17 Wall Street analysis models, has 51 investors with completely different styles each score the stock, then produces a 600KB Bloomberg-style report.

```
/analyze-stock AAPL
```

After 5-8 minutes you get:
- **An HTML report** — self-contained, opens in any browser, works offline
- **A portrait card** — 1080x1920, shareable on social media
- **A landscape card** — 1920x1080
- **A one-liner summary**

## Why Build This

Looking at a single stock used to be: check fundamentals on one app, technicals on another, see what influencers say on a third, dig through broker research, manually build a DCF in Excel... 2-3 hours gone, and you still lose money.

All of this is really just "gather info, analyze from multiple angles, give a verdict." Why not let AI do it all?

Existing tools are either GPT wrappers that output three paragraphs of nothing, or Bloomberg terminals you can't afford. Anthropic's [financial-services-plugins](https://github.com/anthropics/financial-services-plugins) has great methodology (DCF/Comps/LBO), but it's US-only and needs paid data sources (FactSet, S&P Global).

So we built one. **Free data sources only, zero API keys, works with China A-shares out of the box.**

---

## Install

### Claude Code (Plugin)

```bash
/plugin marketplace add wbh604/UZI-Skill
/plugin install stock-deep-analyzer@uzi-skill
```

### Claude Code (Skill)

```bash
git clone https://github.com/wbh604/UZI-Skill.git && pip install -r UZI-Skill/requirements.txt
```

### Codex

```
git clone https://github.com/wbh604/UZI-Skill.git && pip install -r UZI-Skill/requirements.txt && python UZI-Skill/skills/deep-analysis/scripts/run_real_test.py AAPL
```

### Cursor / Windsurf / Devin

Just paste this:

> Clone https://github.com/wbh604/UZI-Skill, install requirements.txt, then follow the 6-Task workflow in `skills/deep-analysis/SKILL.md` to analyze a stock.

### CLI Only

```bash
git clone https://github.com/wbh604/UZI-Skill.git
cd UZI-Skill && pip install -r requirements.txt
python skills/deep-analysis/scripts/run_real_test.py AAPL
```

---

## Usage

| Command | What It Does |
|---|---|
| `/analyze-stock AAPL` | Full 6-Task deep analysis |
| `/dcf 600519` | DCF valuation with 5x5 sensitivity table |
| `/comps 002273` | Peer comparison with percentile ranking |
| `/lbo 600519` | LBO test — PE buyer IRR perspective |
| `/initiate 002273` | Initiating coverage report (JPM/GS style) |
| `/ic-memo 002273` | Investment committee memo with 3 scenarios |
| `/earnings 002273` | Earnings beat/miss analysis |
| `/catalysts 002273` | Catalyst calendar — next 60 days |
| `/thesis 002273` | Investment thesis tracker (5 pillars) |
| `/screen 002273` | 5 quant screens (value/growth/quality) |
| `/dd 002273` | Due diligence checklist (21 items) |
| `/scan-trap 002273` | Scam detection (8 signals) |

---

## 🎭 51 Investor Jury

Not template phrases. Each has their own **quantified rule set** (180 rules total). Every recommendation cites the exact rule it hit:

| Group | Style | Count | Representatives |
|---|---|---|---|
| A | Classic Value | 6 | Buffett · Graham · Munger · Fisher · Templeton · Klarman |
| B | Growth | 4 | Lynch · O'Neil · Thiel · Cathie Wood |
| C | Macro/Hedge | 5 | Soros · Dalio · Howard Marks · Druckenmiller · Robertson |
| D | Technical | 4 | Livermore · Minervini · Darvas · Gann |
| E | China Value | 6 | Duan Yongping · Zhang Kun · Zhu Shaoxing · Xie Zhiyu · Feng Liu · Deng Xiaofeng |
| F | A-Share Day Traders | 23 | Zhang Mengzhu · Zhao Laoge · Foshan Shadowless Kick · Beijing Trader · Xin Duoduo … |
| G | Quant | 3 | Simons · Thorp · David Shaw |

---

## 📐 17 Institutional Methods

Ported from [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins), adapted with A-share parameters:

**Valuation**: DCF · Comps · 3-Statement · LBO · Merger Model

**Research**: Initiating Coverage · Earnings Analysis · Catalyst Calendar · Thesis Tracker · Morning Note · Idea Screen · Sector Overview

**Decision**: IC Memo · Porter 5 Forces + BCG · DD Checklist · Unit Economics · Value Creation Plan · Portfolio Rebalance

---

## 📸 What The Report Looks Like

> All screenshots from a real analysis of Crystal Optech (002273.SZ).

### Score Dashboard
<img src="docs/screenshots/hero-score.png" width="700" />

### The Great Divide — Bull vs Bear
<img src="docs/screenshots/great-divide.png" width="700" />

### 51 Jury Seats
<img src="docs/screenshots/jury-seats.png" width="700" />

### Chat Room Mode
<img src="docs/screenshots/chat-room.png" width="700" />

### DCF Sensitivity Heatmap
<img src="docs/screenshots/dcf-model.png" width="700" />

### IC Memo — 3 Scenarios
<img src="docs/screenshots/ic-memo.png" width="700" />

### 22 Dimension Deep Cards
<img src="docs/screenshots/deep-scan.png" width="700" />

### Social Share Card
<img src="docs/screenshots/share-card.png" width="300" />

---

## ❓ FAQ

**Q: How long does it take?**
A: 5-8 minutes per stock. Most time is data fetching. The modeling itself takes <1 second.

**Q: Do I need paid data sources?**
A: No. All free (akshare / yfinance / DuckDuckGo / cninfo). Zero API keys.

**Q: Does it work for US/HK stocks?**
A: Yes. `/analyze-stock AAPL` or `/analyze-stock 00700.HK`.

**Q: Is this investment advice?**
A: No. This is a tool, not a fortune teller. The 51 investor opinions are rule-engine simulations, not real people's views.

---

## ⭐ Star History

<a href="https://star-history.com/#wbh604/UZI-Skill&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=wbh604/UZI-Skill&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=wbh604/UZI-Skill&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=wbh604/UZI-Skill&type=Date" />
 </picture>
</a>

---

## ⚠️ Disclaimer

This tool generates analysis reports using AI models based on public data. All scores, recommendations, and simulated commentary are algorithm outputs and do not represent any real investor's actual views. **Not investment advice.** Invest at your own risk.

---

<div align="center">

MIT License · Made by FloatFu-true · O.o

</div>
