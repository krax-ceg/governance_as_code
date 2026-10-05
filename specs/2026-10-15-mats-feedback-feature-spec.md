# Feature Spec: Maturity, Pricing & Governance-Body Gaps

Source: feedback call with Mats Stuhrmann, 2026-10-15 (auto-transcribed,
heavily garbled; findings cross-checked against repo state before being
included here). Items already implemented in the repo are explicitly
called out as out of scope rather than re-specified.

## 1. Decision-rights frameworks beyond RACI (DACI / RAPID)

- **Problem:** `governance-as-code/raci/raci-matrix.template.yaml` and the
  Tier 1 maturity assessment only capture RACI. Mats flagged that
  engagements repeatedly need DACI/RAPID-style decision-rights mapping too,
  and that this gap should be surfaced earlier, during the assessment
  phase, not discovered later.
- **Proposed change:** add `daci-matrix.template.yaml` and/or
  `rapid-matrix.template.yaml` alongside the existing RACI template
  (mirroring `governance-as-code/schemas/raci-matrix.schema.json`), and
  reference the new template(s) from the Tier 1 deliverables checklist as
  an alternative/complement to RACI, selected during the maturity
  assessment.

## 2. Interactive maturity/capability wheel for workshops

- **Problem:** `offering/maturity-assessment-instrument.xlsx` produces a
  static score; there's no visual artifact for live workshop facilitation.
- **Proposed change:** add a ring/radar-style "current state vs. target
  state" diagram (with intermediate activities plotted between rings),
  driven off the maturity instrument's output scores, for use in
  `playbook/workshop-agendas/`.

## 3. T-shirt-sized base + option pricing model

- **Problem:** `offering/pricing-tiers.md` only offers fixed-fee 30-day
  tiers; there's no lighter-weight sizing model.
- **Proposed change:** add a T-shirt-sizing packaging option — a "bare
  minimum" base package plus a menu of optional deliverables, priced by
  number of workshops — as an alternative/addition to the existing tier
  structure in `pricing-tiers.md`.

## 4. Immersion program as a post-engagement option

- **Problem:** `offering/pricing-tiers.md` → "Post-Engagement Options"
  only lists the Run-the-Hub retainer and Additional Spoke rollout.
- **Proposed change:** add a third post-engagement option that converts
  the Tier 1 final recommendation into an ongoing "immersion program."

## 5. Governing-document inventory + training module

- **Problem:** no equivalent exists today to the governing-document
  inventory and associated training content Kristian referenced from a
  past client engagement.
- **Proposed change:** add a new playbook component / checklist item for
  inventorying existing governing documents and training materials,
  feeding into the "organizational transformation as code" framing
  (beyond pure compliance) — likely a new subsection in
  `playbook/phase-1-assess-charter.md` or a new
  `offering/governing-document-inventory.md`.

## Out of scope / already implemented (confirmed, not re-specified here)

- Hub/Spoke charter config (`governance-as-code/councils/`)
- GitHub Actions / Azure Pipelines CI with platform auto-detection
  (`governance-as-code/ci/`)
- Data contract / data product templates (`governance-as-code/contracts/`)

## Open questions for Kristian / Mats

- Exact scope of "DACI vs RAPID" — both, or pick one as default?
- Pricing mechanics for T-shirt sizing: do existing tiers get replaced or
  coexist?
- Whether the immersion program is scoped in this doc or needs its own
  pricing workshop first.
