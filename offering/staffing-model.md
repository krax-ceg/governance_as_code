# Staffing Model

## Client-Side Roles (required, not provided by Cegeka)

| Role | Commitment | Responsibility |
|---|---|---|
| Executive Sponsor | ~2 hrs/week | C-suite accountability for the program; chairs Hub escalations |
| Data Governance Manager | Full-time during engagement | Client-side day-to-day owner; chairs Operational Governance Committee post-handover |
| Domain Business Owners | ~2 hrs/week each | One per pilot Spoke; accountable for domain data decisions |
| Data Stewards | ~4 hrs/week each | One per pilot Spoke; day-to-day metadata/contract maintenance |

Tier 1 cannot start without a named Executive Sponsor and Governance Manager — this is a hard gate, not a nice-to-have (see `../playbook/phase-1-assess-charter.md`).

## Cegeka-Side Roles

| Role | Tiers active | Responsibility |
|---|---|---|
| Lead Advisor | 1 (light touch in 2–3) | Client relationship, charter facilitation, board-level ROI narrative |
| Governance Architect | 1, 2, 3 | Designs Hub/Spoke charter, RACI, owns the `governance-as-code/` config for this client |
| Data Engineer | 2 | Asset discovery, PII tagging, data contract drafting, RBAC/masking implementation |
| Platform Engineer | 3 | Schema registry integration, OPA/Rego policy authoring and deployment, CI/CD wiring |

A single Governance Architect can run Tiers 1–3 for a small/single-domain engagement; the Data Engineer and Platform Engineer roles scale with the number of concurrent pilot domains and underlying platforms.

## Staffing Scales With

- Number of concurrent pilot Spokes in Tier 2/3 (roughly +0.5 FTE Data/Platform Engineer per additional domain run in parallel).
- Platform diversity (multi-cloud/multi-platform Tier 3 work needs platform-specific policy authoring, not just one Rego module).
