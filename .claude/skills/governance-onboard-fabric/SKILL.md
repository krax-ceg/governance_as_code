---
name: governance-onboard-fabric
description: Onboard a Microsoft Fabric lakehouse table into the Governance-as-Code Accelerator — introspect tables read-only, generate Open Data Contract Standard (ODCS) and Open Data Product Standard (ODPS) YAML, and scaffold the CI validation pipeline (GitHub Actions or Azure Pipelines, auto-detected from the target repo's git remote). Use when a user asks to "onboard a Fabric table/lakehouse to governance," "generate a data contract for this Fabric table," or "wire up governance-as-code for Fabric."
---

# Governance Onboarding — Microsoft Fabric

Generates governance-as-code artifacts for a Microsoft Fabric lakehouse table without writing anything back to Fabric. This skill is **read-only scaffolding**: it introspects table/schema metadata via the Fabric REST API and produces files (contracts, products, CI config) for human review and commit — it does not assign workspace roles, apply Purview sensitivity labels, or alter anything in the live workspace. Full read+write (applying those policies back to Fabric) is an explicit non-goal of this first release — see `governance-as-code/schemas/core10-and-31-attribute-framework.md` and the offering gap analysis for why.

## When to use this

- A consultant or client platform engineer wants to bring an existing Fabric lakehouse table under governance (generate its first data contract).
- Onboarding a new pilot domain's tables during Phase 2 of the playbook (`../../playbook/phase-2-map-secure.md`) for a client on Fabric rather than Databricks.
- Re-generating a contract after a schema change, to diff against the previously committed version (SemVer bump decision is a human call — this skill drafts, it doesn't auto-bump).

## Prerequisites

- `pip install requests pyyaml jsonschema jinja2` (shared across both platform skills — no Fabric-specific SDK is required, this uses the plain REST API).
- Environment variable `FABRIC_TOKEN` set to an Azure AD bearer token with **read-only** Fabric API scope (e.g. obtained externally via `az account get-access-token --resource https://api.fabric.microsoft.com` and exported by the operator — this skill does not invoke the Azure CLI itself). Never pass the token as a CLI flag or commit it.
- The operator must have on hand the five Core-10 fields no API can supply: data owner (name+email), data steward (name+email), classification tier, criticality tier, and support channel. See `../../governance-as-code/schemas/core10-and-31-attribute-framework.md`.

## Invocation sequence

1. **Introspect** the target table(s) (read-only):
   ```bash
   python scripts/introspect_fabric_workspace.py \
     --workspace-id <workspace_guid> --lakehouse-id <lakehouse_guid> \
     --table factory_lead_times \
     --out introspected_table.json
   ```
   Or `--all-tables --out-dir introspected/` for the whole lakehouse.

2. **Collect operator input** — same five Core-10 fields as the Databricks skill, written to a small JSON file:
   ```json
   {
     "data_owner": {"name": "...", "email": "..."},
     "data_steward": {"name": "...", "email": "..."},
     "classification": "restricted",
     "criticality": "tier-1",
     "support_channel": "#help-<domain>-data"
   }
   ```

3. **Generate the ODCS contract**:
   ```bash
   python ../governance_core/generate_odcs_contract.py \
     --table introspected_table.json --operator-input operator_input.json \
     --out ../../governance-as-code/contracts/<asset_name>.contract.yaml
   ```

4. **Generate the ODPS product** (group one or more contracts):
   ```bash
   python ../governance_core/generate_odps_product.py \
     --contract ../../governance-as-code/contracts/<asset_name>.contract.yaml \
     --product-name "<Human Product Name>" \
     --owner-name "<owner>" --owner-email "<email>" \
     --platform fabric --location "<workspace>/<lakehouse>/<table>" \
     --out ../../governance-as-code/contracts/<product_slug>.product.yaml
   ```

5. **Validate locally** before committing:
   ```bash
   python ../../governance-as-code/ci/validate_yaml.py \
     --schema ../../governance-as-code/schemas/odcs-data-contract.schema.json \
     ../../governance-as-code/contracts/<asset_name>.contract.yaml
   ```

6. **Detect the target repo's CI system and scaffold validation** (run inside the *client's* repo, not this accelerator repo):
   ```bash
   python ../governance_core/detect_git_remote.py --repo .
   # github       -> python ../governance_core/emit_github_actions.py --target-repo .
   # azure-devops -> python ../governance_core/emit_azure_pipelines.py --target-repo .
   # unknown      -> ask the operator which CI system to scaffold for
   ```
   Fabric engagements more often sit on Azure DevOps than GitHub — don't assume; always detect.

7. **(Optional) Bridge into the PBAC schema-registry policy** already in this repo:
   ```bash
   python ../governance_core/odcs_to_policy_input.py \
     --contract ../../governance-as-code/contracts/<asset_name>.contract.yaml \
     --out policy_input.json
   # then: opa eval -i policy_input.json -d ../../governance-as-code/policies/data-contracts/contract-validation.rego \
   #         'data.gac.data_contracts.validation.valid'
   ```

8. Commit the generated contract/product/CI files on a feature branch and open a PR for human review — generated governance artifacts go through the same review process as application code.

## What this skill will not do

- Will not assign Fabric workspace roles or Purview sensitivity labels.
- Will not auto-decide a SemVer bump on re-generation — flag the diff to the user and let them decide MAJOR/MINOR/PATCH per `../../playbook/` Section 4.2 rules.
- Will not fabricate Core-10 fields (owner/steward/classification/criticality/support channel) — always ask the operator.
