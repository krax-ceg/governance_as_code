# Governance-as-Code Accelerator

A packaged Cegeka Nordic advisory offering: a standardized, repeatable engagement for installing a **federated Hub-and-Spoke data governance model** — with the organizational structures (charters, councils, RACI) *and* the technical controls (PBAC, data contracts) delivered as versioned, testable code, not just a slide deck.

Source strategy report that informed this offering: `vcc_report_v6_2026-06-24.html` (internal, confidential — not included in this repo).

## How the Four Parts Fit Together

| Folder | Audience | Purpose |
|---|---|---|
| `sales/` | Prospective clients | Client-facing one-pager/brochure for pitching the offering |
| `offering/` | Sales & delivery leads | Internal definition of scope, pricing tiers, staffing model, sign-off checklist |
| `playbook/` | Delivery team | Phase-by-phase runbook and workshop agendas to actually deliver the engagement |
| `governance-as-code/` | Delivery team + client's platform team | The literal, forkable starter kit: YAML charter/RACI templates, OPA/Rego policies, CI validation — this is what gets forked into the client's own repo and handed over at the end |

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
