# Phase 3 (Days 61–90): Automate & Scale

**Goal:** introduce real-time automation and move from the Phase 2 manual baseline to a full Policy-Based Access Control (PBAC) model, with programmatic, auditable enforcement.

**Gate to start:** Phase 2 exit checklist signed off (data contracts drafted, baseline RBAC + masking live).

## Days 61–70: Registry Integration

- Configure schema registries to automatically validate events against the Phase 2 data contracts.
- Reject payloads that violate the contract at ingestion time — see `../governance-as-code/policies/data-contracts/contract-validation.rego` for the reference policy.

## Days 71–80: JIT Access Automation

- Implement just-in-time (JIT) access workflows to replace the Phase 2 static RBAC groups with time-limited, task-specific credentials.
- Deploy `../governance-as-code/policies/pbac/access-policy.rego` and `jit-access.rego`; wire into the client's identity/access platform.

## Days 81–90: Programmatic Audit & Review

- Move metric definitions into the version-controlled `governance-as-code/` repo (now forked into the client's own org).
- Wire `../governance-as-code/ci/github-actions/validate-governance-config.yml` into the client's CI so governance config changes are linted and policy-tested on every PR, not just at handover.
- Conduct the first programmatic compliance audit using the deployed policies; publish the first departmental governance scorecard.

**Exit gate:** see `../offering/deliverables-checklist.md` Tier 3 section, then proceed to Handover.

## After Day 90: Scale-Out

Each additional Spoke domain reuses the Hub infrastructure built in Phase 1–3 — onboarding cost per additional domain is materially lower than the original build (see `../offering/pricing-tiers.md`, "Additional Spoke rollout").
