# Pricing & Tiering

Three tiers, each a 30-day block, mapped to the delivery playbook (`../playbook/`). Each tier ends in a client sign-off gate — the client can stop after any tier with a working, documented deliverable; nothing is held hostage to "buy the next phase."

| Tier | Duration | Fee basis | Core team | Primary deliverable |
|---|---|---|---|---|
| **Tier 1 — Assess & Charter** | ~30 days | Fixed fee | 1 Lead Advisor + 1 Governance Architect (part-time) | Signed Hub/Spoke Charter, RACI matrix, committee cadence established |
| **Tier 2 — Map & Secure** | ~30 days | Fixed fee | 1 Governance Architect + 1 Data Engineer | Asset inventory, pilot data contracts (YAML), baseline RBAC + masking live |
| **Tier 3 — Automate & Scale** | ~30 days | Fixed fee + T&M for scale-out beyond pilot domain | 1 Governance Architect + 1 Platform Engineer | Schema registry validation, PBAC/JIT policies (OPA) in production, first programmatic audit |

## Packaging Options

- **Full Accelerator (Tiers 1–3, ~90 days):** recommended default — this is the pricing anchor; priced at a discount vs. buying tiers individually.
- **Tier 1 standalone ("Governance Assessment & Charter"):** lower-commitment entry point for clients who are governance-skeptical or need board buy-in before committing further. Common upsell path into Tiers 2–3.
- **Tier 3 as standalone add-on:** for clients who already have organizational governance (charters, councils) in place but need the technical automation layer (PBAC/JIT, schema validation) — requires a 2-day gap assessment to confirm Tier 1/2 prerequisites are actually met before quoting.

## What Drives Price Variance

- Number of pilot domains/Spokes in scope (base price assumes one pilot domain; each additional concurrent domain in Tier 2–3 is an add-on line item).
- Underlying platform(s) already in place (single platform vs. multi-platform / multi-cloud increases Tier 3 integration effort).
- Regulatory complexity (GDPR-only vs. additional sector-specific regimes) affects Tier 2 PII/compliance mapping effort.

## Post-Engagement Options

- **Run-the-Hub retainer:** ongoing advisory seat on the client's Hub council plus quarterly governance config review (not included in the three tiers above).
- **Additional Spoke rollout:** fixed-fee package to onboard each subsequent domain onto the already-built Hub using the starter kit — materially cheaper than the original Tier 2–3 work since the Hub infrastructure already exists.

*(Rate card and absolute figures intentionally omitted here — pull current Cegeka Nordic advisory rate card at proposal time.)*
