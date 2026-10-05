# Workshop: RACI Mapping

**When:** Days 11–20 of Phase 1. **Duration:** half-day. **Attendees:** Data Governance Manager, Domain Business Owner(s), candidate Data Steward(s), Cegeka Governance Architect.

## Choosing a decision-rights framework

RACI is the default for this workshop. Two alternatives exist for domains
where RACI doesn't fit the client's actual decision shape — pick one
framework per domain, not a mix:

- **DACI** (`../../governance-as-code/raci/daci-matrix.template.yaml`) —
  better fit when decisions are initiative/approval-shaped (a proposal is
  driven to a recommendation, then approved), rather than ongoing
  operational work.
- **RAPID** (`../../governance-as-code/raci/rapid-matrix.template.yaml`) —
  better fit when the client has a heavier cross-functional sign-off chain
  with several roles able to veto before a decision is final.

Decide which framework to use for the domain before working through the
decision types below — switching mid-workshop wastes the room's time.

## Objectives

1. Assign roles for each governance decision type, per the chosen
   framework (Responsible/Accountable/Consulted/Informed for RACI;
   Driver/Approver/Contributors/Informed for DACI;
   Recommend/Agree/Perform/Input/Decide for RAPID).
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
| 0:00–0:10 | Recap: why a documented decision-rights framework, not just an org chart — ambiguity here is the #1 cause of Phase 2 delays |
| 0:10–1:00 | Work through each decision type, assign roles per the chosen framework, resolve disagreements live |
| 1:00–1:20 | Confirm Data Steward has real authority (can they actually approve a contract, or does it silently escalate every time?) |
| 1:20–1:30 | Record final matrix into the chosen framework's template under `../../governance-as-code/raci/` |

## Output

- Decision-rights matrix YAML completed (RACI, DACI, or RAPID — whichever
  was chosen for this domain) and reviewed by all named owners.
- Any unresolved disagreements escalated to the Executive Sponsor before Phase 1 exit.
