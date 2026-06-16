# 🔬 deep-insight

> "The important thing in science is not so much to obtain new facts as to discover new ways of thinking about them." — William Lawrence Bragg

**Deep Insight** is a skill repository for the [yogsoth-ai](https://github.com/yogsoth-ai) ecosystem that transforms surface-level research gaps into deep structural understanding. It orchestrates 5 analytical campaigns — gap analysis, insight generation, boundary analysis, sensitivity analysis, and problem reformulation — to produce research insights that go beyond literature review into genuine understanding.

> 🧭 **Part of the [De-Anthropocentric Research Engine](https://github.com/yogsoth-ai/de-anthropocentric-research-engine).** This repository is one of nine composable research packages that make up DARE — the full autonomous research-orchestration system. DARE bundles this package together with the others into a single self-contained clone, unified under one orchestrator. To use these skills as intended — with the spec-driven orchestrator and cross-package routing — clone the [main repository](https://github.com/yogsoth-ai/de-anthropocentric-research-engine) rather than this repo alone.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENTRY.md                                  │
│                   (Campaign Router)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────┐  ┌───────────────────────────┐  │
│  │ gap-analysis │  │ insight  │  │ boundary-analysis         │  │
│  │  5 strat     │  │ 5 strat  │  │  5 strat                  │  │
│  │  3 tactic    │  │ 4 tactic │  │  3 tactic                 │  │
│  │ 11 SOP       │  │ 14 SOP   │  │ 12 SOP                    │  │
│  └──────────────┘  └──────────┘  └───────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────┐  ┌────────────────────────────┐   │
│  │ sensitivity-analysis     │  │ problem-reformulation      │   │
│  │  5 strat                 │  │  5 strat                   │   │
│  │  3 tactic                │  │  3 tactic                  │   │
│  │ 11 SOP                   │  │ 10 SOP                     │   │
│  └──────────────────────────┘  └────────────────────────────┘   │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Shared: 5 import SOPs + 3 shared subagent SOPs            │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Scale

| Layer | Count |
|-------|-------|
| Campaigns | 5 |
| Strategies | 25 |
| Tactics | 16 |
| SOPs (subagent) | 58 |
| SOPs (import) | 5 |
| SOPs (shared) | 3 |
| **Total skill directories** | **111** |

## Quick Start

```bash
# Clone
git clone https://github.com/yogsoth-ai/deep-insight.git

# Configure MCP servers (copy and fill in API keys)
cp .mcp.example.json .mcp.json

# Use via Claude Code or compatible agent
# Entry point: ENTRY.md routes to campaigns based on research phase
```

## Campaigns

**Gap Analysis** — Identify, validate, and prioritize research gaps. Distinguishes genuine opportunities from already-solved problems, measures feasibility and impact, ranks by multi-criteria scoring.

**Insight** — Transform gaps into deep structural understanding. Applies root-cause drilling, stakeholder mapping, tension mining, question reformulation, abstraction laddering, and assumption auditing.

**Boundary Analysis** — Map the validity envelope of research approaches. Determines where methods work, where they break, and what drives the transition. Uses validity envelope mapping, failure mode analysis, and contextual boundary detection.

**Sensitivity Analysis** — Quantify which assumptions and parameters matter. Screens parameters, decomposes variance, tests assumption criticality, propagates uncertainty, and identifies decision-sensitive factors.

**Problem Reformulation** — Question the problem itself. Escapes dominant paradigms, reframes from multiple perspectives, applies dialectical inquiry, assesses wickedness, and discovers appreciative alternatives.

## Dependencies

This skill repo imports SOPs from sibling yogsoth-ai repositories:

| Dependency | SOPs Imported |
|-----------|---------------|
| [web-browsing](https://github.com/yogsoth-ai/web-browsing) | web-search, web-research |
| [literature-engine](https://github.com/yogsoth-ai/literature-engine) | paper-overview, paper-search, paper-research |
| [subagent-spawning](https://github.com/yogsoth-ai/subagent-spawning) | spawn-agent (execution runtime) |
| [context-management](https://github.com/yogsoth-ai/context-management) | context-checkpoint (state persistence) |

## 📄 License

[Apache-2.0](LICENSE)

---

*A component of the [De-Anthropocentric Research Engine](https://github.com/yogsoth-ai/de-anthropocentric-research-engine), part of the [Yogsoth AI](https://github.com/yogsoth-ai) ecosystem. Built by [Pthahnix](https://github.com/Pthahnix).*
