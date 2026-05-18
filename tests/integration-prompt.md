# Integration Test Scenarios

7 test scenarios covering each campaign + cross-campaign orchestration.

---

## 1. Gap Identification

**Invoke:** gap-analysis → gap-identification
**Expect:** paper-overview + web-search budget consumption, gap-keyword-extraction subagent spawned
**Verify:**
- [ ] State Ledger updates after each SOP call
- [ ] Budget Gate enforced (>=80% before exit)
- [ ] gap-keyword-extraction produces structured output

---

## 2. Gap Validation + Prioritization

**Invoke:** gap-analysis → gap-validation → gap-prioritization
**Expect:** cross-database-verification + multi-criteria-scoring subagents spawned
**Verify:**
- [ ] cross-database-verification checks multiple sources
- [ ] multi-criteria-scoring produces ranked gap list
- [ ] gap-validation-matrix tactic minimum yield met

---

## 3. Root Cause Insight

**Invoke:** insight → root-cause-drilling
**Expect:** five-whys-drilling + causal-tree-construction + CLR-validation subagents
**Verify:**
- [ ] five-whys-drilling reaches 5 levels deep
- [ ] causal-tree-construction produces valid tree structure
- [ ] CLR-validation confirms or rejects the root cause

---

## 4. Boundary Analysis

**Invoke:** boundary-analysis → validity-envelope-mapping
**Expect:** variation-axis-identification + systematic-perturbation + envelope-construction subagents
**Verify:**
- [ ] At least 3 variation axes identified
- [ ] Perturbation covers each axis
- [ ] Envelope construction produces boundary description

---

## 5. Sensitivity Analysis

**Invoke:** sensitivity-analysis → assumption-criticality
**Expect:** assumption-extraction + negation-definition + re-derivation + conclusion-sensitivity-measurement
**Verify:**
- [ ] At least 5 assumptions extracted
- [ ] Negations are "strongest plausible alternative" not logical NOT
- [ ] Sensitivity ranking produced with critical/safe classification

---

## 6. Problem Reformulation

**Invoke:** problem-reformulation → dominant-idea-escape
**Expect:** dominant-idea-identification + provocation-generation + consequence-following
**Verify:**
- [ ] Dominant ideas identified with evidence of dominance
- [ ] 4+ provocations (one per technique)
- [ ] Consequence chains followed 3-5 steps
- [ ] At least 1 viable new framing extracted

---

## 7. Multi-Campaign Orchestration

**Route:** gap-analysis → insight → boundary-analysis → problem-reformulation
**Verify:**
- [ ] Context checkpoint saved between campaigns
- [ ] Outputs from earlier campaigns inform later ones
- [ ] ENTRY.md routing selects correct campaign based on signals
- [ ] Budget Gates enforced at each strategy level
- [ ] Final output integrates findings across all campaigns
