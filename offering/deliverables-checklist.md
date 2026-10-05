# Deliverables Checklist & Sign-Off Gates

Each tier ends with a client sign-off against this checklist. Use this as the exit-criteria section of the SOW.

## Tier 1 — Assess & Charter (Days 1–30)

- [ ] Maturity assessment completed (`../offering/maturity-assessment-instrument.xlsx`) and recommended starting Wave agreed with the client
- [ ] Executive Sponsor and Data Governance Manager formally appointed (named individuals, not roles)
- [ ] Operational Governance Committee Charter drafted and signed, including voting mechanics
- [ ] Domain Business Owners and Data Stewards identified for the pilot Spoke(s)
- [ ] RACI matrix completed and reviewed by all named owners (`governance-as-code/raci/raci-matrix.template.yaml` instantiated)
- [ ] Hub and pilot Spoke charters instantiated from templates (`governance-as-code/councils/`) and ratified
- [ ] First Operational Committee session held; meeting cadence set

## Tier 2 — Map & Secure (Days 31–60)

- [ ] Metadata scan complete for pilot domain(s); sensitive/PII attributes tagged
- [ ] Lineage dependencies mapped for in-scope pipelines
- [ ] At least one pilot data contract drafted in YAML (ODCS format — generated via the Databricks/Fabric onboarding skill where the pilot platform is one of those two, see `.claude/skills/`) and reviewed by domain Data Steward
- [ ] Baseline RBAC groups aligned to non-overlapping roles
- [ ] Column-level masking live on tagged sensitive datasets

## Tier 3 — Automate & Scale (Days 61–90)

- [ ] Schema registry validating events against data contracts; non-conformant payloads rejected
- [ ] PBAC/JIT access policies (`governance-as-code/policies/pbac/`) deployed and tested in client environment
- [ ] CI pipeline (`governance-as-code/ci/github-actions/validate-governance-config.yml`) running against the client's forked config repo
- [ ] First programmatic compliance audit executed and reviewed with Executive Sponsor
- [ ] Departmental governance scorecard published at least once

## Handover

- [ ] Client's platform team has forked/owns the `governance-as-code/` repo
- [ ] Run-the-Hub retainer discussed (accept/decline documented)
- [ ] Additional Spoke rollout roadmap discussed, if applicable
