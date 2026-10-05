# Workshop: RACI Mapping

**When:** Days 11–20 of Phase 1. **Duration:** half-day. **Attendees:** Data Governance Manager, Domain Business Owner(s), candidate Data Steward(s), Cegeka Governance Architect.

## Objectives

1. Assign Responsible / Accountable / Consulted / Informed for each governance decision type.
2. Confirm Data Stewards have the authority their role requires (not just the title).

## Decision Types to Map (minimum set — extend per client)

- Schema addition/change to a Spoke's local assets
- Schema addition/change to the shared/global catalog
- New data contract approval
- Cross-domain metric collision resolution
- Access grant/revocation (non-JIT, Phase 1–2 baseline)
- Sensitive/PII tagging sign-off

## Agenda

| Time | Item |
|---|---|
| 0:00–0:10 | Recap: why RACI, not just an org chart — ambiguity here is the #1 cause of Phase 2 delays |
| 0:10–1:00 | Work through each decision type, assign R/A/C/I, resolve disagreements live |
| 1:00–1:20 | Confirm Data Steward has real authority (can they actually approve a contract, or does it silently escalate every time?) |
| 1:20–1:30 | Record final matrix into `../../governance-as-code/raci/raci-matrix.template.yaml` |

## Output

- RACI matrix YAML completed and reviewed by all named owners.
- Any unresolved disagreements escalated to the Executive Sponsor before Phase 1 exit.
