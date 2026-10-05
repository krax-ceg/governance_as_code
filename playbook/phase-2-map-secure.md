# Phase 2 (Days 31–60): Map & Secure

**Goal:** translate the organizational structures ratified in Phase 1 into technical configuration and establish a security baseline. This phase deliberately stops short of full automation (PBAC/JIT) — see Phase 3 — to avoid "operational paralysis" from deploying everything at once.

**Gate to start:** Phase 1 exit checklist signed off (charters ratified, RACI complete, committee cadence running).

## Days 31–40: Asset Discovery

- Deploy metadata scanners across the pilot Spoke's datasets; index and tag sensitive/PII attributes.
- Map lineage dependencies for in-scope pipelines.
- Output feeds the data contract schema (`../governance-as-code/schemas/`) and the Spoke charter's declared data asset inventory.

## Days 41–50: Pilot Data Contracts

- Select 1–3 high-value ingestion pipelines in the pilot domain.
- Draft initial YAML-based data contracts with the domain Data Steward — contract schema validated against `../governance-as-code/schemas/` (extend as needed for client-specific fields).
- Review contracts with the Spoke council before moving to Phase 3 enforcement.

## Days 51–60: Baseline Access Control

- Align standard user accounts with non-overlapping RBAC groups — this is the manual baseline that PBAC (Phase 3) will later replace with policy-driven, time-limited access.
- Implement column-level masking on datasets tagged sensitive in Days 31–40.

**Exit gate:** see `../offering/deliverables-checklist.md` Tier 2 section. Client sign-off required before Tier 3 kickoff.
