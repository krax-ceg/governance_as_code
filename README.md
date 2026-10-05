# Governance-as-Code Accelerator

A packaged Cegeka Nordic advisory offering: a standardized, repeatable engagement for installing a **federated Hub-and-Spoke data governance model** — with the organizational structures (charters, councils, RACI) *and* the technical controls (PBAC, data contracts) delivered as versioned, testable code, not just a slide deck.

Source strategy report that informed this offering: `vcc_report_v6_2026-06-24.html` (internal, confidential — not included in this repo).

## How the Parts Fit Together

| Folder | Audience | Purpose |
|---|---|---|
| `sales/` | Prospective clients | Client-facing one-pager/brochure for pitching the offering, incl. differentiation vs. catalog tools (Collibra/Purview/Atlan/Immuta) |
| `offering/` | Sales & delivery leads | Internal definition of scope, pricing tiers, staffing model, sign-off checklist, and the deterministic maturity-assessment instrument used in Tier 1 |
| `playbook/` | Delivery team | Phase-by-phase runbook and workshop agendas to actually deliver the engagement |
| `governance-as-code/` | Delivery team + client's platform team | The literal, forkable starter kit: YAML charter/RACI templates, OPA/Rego policies, ODCS/ODPS contract &amp; product templates, CI validation (GitHub Actions and Azure Pipelines) — this is what gets forked into the client's own repo and handed over at the end |
| `.claude/skills/` | Delivery team (via Claude Code) | Agentic skills that generate the `governance-as-code/contracts/` artifacts from a live Databricks or Fabric environment and scaffold the matching CI pipeline — see **Platform Onboarding Skills** below |

This repo's structure closes the four gaps identified in the internal offering gap analysis (enumerated metadata framework, reusable automation, commercial packaging, deterministic scoring) — see `governance-as-code/schemas/core10-and-31-attribute-framework.md` for the first of those four.

## Platform Onboarding Skills (Databricks &amp; Fabric)

`.claude/skills/governance-onboard-databricks/` and `.claude/skills/governance-onboard-fabric/` are Claude-Code-invokable skills that turn a live lakehouse schema into governance-as-code artifacts:

1. **Introspect** the target platform read-only (Unity Catalog REST/SDK, or the Fabric REST API) — no grants, no writes, no live credentials beyond read access.
2. **Generate** an Open Data Contract Standard (ODCS) contract and an Open Data Product Standard (ODPS) product descriptor into `governance-as-code/contracts/`, populated against the Core 10 / 31-attribute framework.
3. **Detect** whether the target repo's git remote is GitHub or Azure DevOps (`.claude/skills/governance_core/detect_git_remote.py`) and scaffold the matching CI validation pipeline — `.github/workflows/governance-as-code.yml` or `azure-pipelines.yml`.
4. **Bridge** the generated ODCS contract into the existing `governance-as-code/policies/data-contracts/contract-validation.rego` schema-registry policy via `odcs_to_policy_input.py`, so the new artifacts and the already-tested policy layer interoperate without rewriting either.

Read each skill's `SKILL.md` before running it — in particular the "What this skill will not do" section. This first release is intentionally scoped to exactly two platforms; see the skill files for why.

## Quickstart (for delivery teams)

1. Read `offering/offering-overview.md` for the pitch and `playbook/phase-1-assess-charter.md` to start Tier 1.
2. Fork `governance-as-code/` into a new repo under the client's org.
3. Instantiate `governance-as-code/councils/hub-charter.yaml` and a copy of `spoke-charter.template.yaml` per pilot domain during the Chartering Kickoff workshop (`playbook/workshop-agendas/chartering-kickoff.md`). See `governance-as-code/examples/procurement-spoke/` for a filled-in reference.
4. Validate configs locally before committing:
   ```bash
   python governance-as-code/ci/validate_yaml.py \
     --schema governance-as-code/schemas/council-charter.schema.json \
     governance-as-code/councils/hub-charter.yaml
   opa test governance-as-code/policies
   ```
5. Wire `governance-as-code/ci/github-actions/validate-governance-config.yml` into the client's CI once their repo fork exists (Phase 3, Days 81–90).

## Status

First-pass scaffold — enough to pitch, pilot, and run a first client engagement. Extend `governance-as-code/policies/` and the JSON Schemas as client-specific requirements surface; keep the playbook and offering docs in sync with the three-tier structure if the delivery model changes.

Known limitation: the Databricks/Fabric skills are read-only scaffolding (introspect + generate files) — they do not apply PBAC/masking policy changes back to the live platform. Applying generated policy automatically is a deliberate non-goal of this release, not an oversight; revisit once the generate-only workflow has been validated on a real engagement.
