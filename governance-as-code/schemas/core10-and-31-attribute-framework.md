# Core 10 & the 31-Attribute Metadata Framework

> **Provenance note:** the source strategy report (`vcc_report_v6_2026-06-24.html`) refers repeatedly to a "Core 10" metadata gate and a "31-attribute framework" but never enumerates either. This document is a **Cegeka-authored standardization** that fills that gap — it is not a reconstruction of an undisclosed client list. Treat it as the canonical field list this accelerator's tooling (schemas, CI gate, and the Databricks/Fabric onboarding skills in `.claude/skills/`) is built against. Extend it per-client, but don't fork it silently — changes here are a Central Hub decision (see `../councils/hub-charter.yaml`).

## How the two tiers are used

| Tier | Purpose | Enforced by |
|---|---|---|
| **Core 10** | The minimum fields a data contract must carry to be promoted past the CI gate (Bronze → Gold). Missing any of these blocks the PR. | `governance-as-code/schemas/odcs-data-contract.schema.json` (`required`), CI workflow |
| **Full 31** | Catalog-grade metadata expected once an asset is a registered Gold Enterprise Data Product. Not all 31 are required at first ingestion — they accumulate through Phase 2–3 of the playbook. | Same schema, as optional properties; scored in the maturity assessment instrument (`../../offering/maturity-assessment-instrument.xlsx`) |

## Core 10 (CI-blocking gate)

| # | Attribute | ODCS field | Why it blocks |
|---|---|---|---|
| 1 | Unique asset identifier | `metadata.id` (URN) | Nothing else can be referenced, versioned, or governed without a stable ID. |
| 2 | Contract version | `metadata.version` (SemVer) | Without SemVer, consumers can't detect breaking vs. additive changes (see Section 4.2 of the source report). |
| 3 | Lifecycle status | `metadata.status` | Distinguishes active/deprecated/retired — prevents consumption of a dead contract. |
| 4 | Owning domain / Spoke | `accountability.domain` | Routes schema-change approval to the correct Spoke Council. |
| 5 | Data owner (name + email) | `accountability.data_owner` | Single accountable human — matches the RACI "exactly one Accountable" rule. |
| 6 | Data steward (name + email) | `accountability.data_steward` | Day-to-day metadata/contract maintainer, distinct from the accountable owner. |
| 7 | Classification tier | `security_and_privacy.classification` | Drives PBAC sensitivity checks (`../policies/pbac/access-policy.rego`). |
| 8 | Criticality tier | `accountability.criticality` | Determines audit frequency and incident-response SLA. |
| 9 | Schema definition (required fields + types) | `schema.required`, `schema.properties` | The structural contract itself — no schema, no contract. |
| 10 | Support channel | `accountability.support_channel` | Where a consumer reports a break — required before Gold promotion. |

## Full 31-Attribute Framework

Core 10 above, plus 21 additional fields grouped by category:

**Semantic & business context (11–14)**
11. `semantics.business_glossary_link` — link to the canonical business-term definition.
12. `semantics.business_definition` — plain-language definition of the asset (surfaces semantic mismatches like the "Lead Time" case in Section 3.4 of the source report).
13. `semantics.calculation_logic` — for derived metrics, the formula/transformation applied.
14. `semantics.units_of_measurement` — explicit units per numeric field (prevents silent unit-mismatch errors).

**Lineage & lifecycle (15–19)**
15. `metadata.source_system_id` — originating system.
16. `metadata.data_residency_region` — for data-sovereignty/GDPR scoping.
17. `lifecycle.effective_from` — date the contract version became active.
18. `lifecycle.deprecation_date` — planned retirement date, if any.
19. `lifecycle.superseded_by` — URN of the replacement contract, if deprecated.

**Structural integrity (20–23)**
20. `config.grain_keys` — columns constituting the append grain (protects dedup/joins — Section 3.8.4).
21. `config.source_feeds` — upstream feeds that must all be present for completeness (Section 3.8.4).
22. `config.partition_keys` — physical partitioning columns.
23. `config.primary_key` — logical primary key, if distinct from grain keys.

**Quality & SLA (24–27)**
24. `service_level_agreement.update_frequency`
25. `service_level_agreement.max_latency_minutes`
26. `service_level_agreement.target_availability_percentage`
27. `quality_rules.drift_thresholds` — K-S test p-value / PSI thresholds (Section 4.3) that trigger quarantine.

**Security & privacy (28–30)**
28. `security_and_privacy.pii_fields` — per-field PII classification.
29. `security_and_privacy.masking_rules` — masking method + retention period per PII field.
30. `security_and_privacy.access_policy_ref` — ID of the PBAC policy (`../policies/pbac/access-policy.rego`) governing this asset.

**Operational (31)**
31. `accountability.team.members` — full team roster (not just owner/steward) for on-call/escalation routing.

## Relationship to the generated artifacts

The Databricks and Fabric onboarding skills (`.claude/skills/governance-onboard-databricks/`, `.claude/skills/governance-onboard-fabric/`) populate Core 10 automatically where introspectable (asset ID, schema, source system) and prompt the operator for the remainder (owner, steward, classification, criticality, support channel) — these five cannot be inferred from the platform and must come from a human during onboarding. See `../contracts/data-contract.template.yaml` for the resulting shape.
