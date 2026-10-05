# Phase 1 (Days 1–30): Assess & Charter

**Goal:** establish the legal and organizational structures necessary to support programmatic governance before any technical work begins. Skipping this phase to "get to the code faster" is the most common cause of Accelerator engagements stalling in Tier 2 — without a named, accountable owner, nobody can sign off a data contract or an access policy.

**Gate to start:** Executive Sponsor and Data Governance Manager named (see `../offering/staffing-model.md`). Do not begin Tier 1 billing until both are confirmed in writing.

## Days 1–10: Appoint Leadership

- Formally appoint the Executive Sponsor (C-suite) and Data Governance Manager.
- Draft the core Operational Governance Committee Charter — this is the Hub charter; instantiate from `../governance-as-code/councils/hub-charter.yaml`.
- Specify voting mechanics (default: 2/3 majority for global metadata schema or standard-protocol changes — see the YAML template for the configurable threshold).
- Run the governing-document inventory (`../offering/governing-document-inventory.md`) in parallel — existing policies, prior charters, and training materials need to be surfaced before the Hub charter is ratified, so it doesn't conflict with or silently duplicate something that already has institutional buy-in.

**Workshop:** `workshop-agendas/chartering-kickoff.md`

## Days 11–20: Accountability Mapping

- Identify domain Business Owners and appoint Data Stewards for the pilot Spoke(s).
- Choose a decision-rights framework per domain — RACI by default, or DACI/RAPID where it fits the client's decision shape better (see `workshop-agendas/raci-mapping-workshop.md`).
- Build the matrix using the chosen template: `../governance-as-code/raci/raci-matrix.template.yaml`, `daci-matrix.template.yaml`, or `rapid-matrix.template.yaml` — one entry per governance decision type (schema change, access grant, metric certification, cross-domain arbitration).

**Workshop:** `workshop-agendas/raci-mapping-workshop.md`

## Days 21–30: Cadence Launch

- Convene the first session of the Operational Governance Committee; align on first-quarter priorities.
- Establish standard meeting rhythms (recommended: Hub committee biweekly, Spoke council weekly during pilot).
- Instantiate the pilot Spoke charter from `../governance-as-code/councils/spoke-charter.template.yaml`.

**Exit gate:** see `../offering/deliverables-checklist.md` Tier 1 section. Client sign-off required before Tier 2 kickoff.
