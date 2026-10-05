# Governing-Document Inventory & Training Module

Part of the "organizational transformation as code" positioning: the
Accelerator doesn't only encode technical compliance (contracts, policies,
CI) — it also has to account for the client's existing governing documents
and the training that sits around them, or the new Hub/Spoke charters will
contradict or duplicate material nobody told Cegeka about.

## Why this exists

Clients arrive with a pre-existing patchwork of policies, standards, and
training decks — data classification policies, prior data governance
charters, compliance handbooks, onboarding decks. Skipping an inventory of
this material risks the new charter (`governance-as-code/councils/`)
conflicting with, or redundantly re-authoring, something that already has
institutional buy-in. This closes that gap and is run alongside chartering
kickoff (`../playbook/phase-1-assess-charter.md`, Days 1–10).

## Inventory checklist

- [ ] All existing data governance policies, standards, and handbooks
      identified and collected (owner, last review date, current status —
      active / stale / superseded).
- [ ] Any prior governance charters or committee terms of reference
      identified, with a note on whether they're still in force.
- [ ] Existing training materials (onboarding decks, LMS modules,
      compliance training) identified and mapped to the roles in
      `../offering/staffing-model.md`.
- [ ] Conflicts or overlaps between inventoried documents and the new
      Hub/Spoke charter flagged before the charter is ratified.
- [ ] Decision recorded per inventoried document: retire, supersede with
      the new charter, or keep in force alongside it.

## Training module

- [ ] Gap identified between existing training materials and the roles
      defined in the new operating model (Data Steward, Domain Business
      Owner, etc.).
- [ ] A short enablement session or updated training material drafted to
      cover any newly introduced roles/responsibilities and, where used,
      the decision-rights framework in play (RACI, DACI, or RAPID — see
      `../governance-as-code/raci/`).
- [ ] Training delivery owner named (client Data Governance Manager by
      default — see `staffing-model.md`).

## Related artifacts in this repo

- `../playbook/phase-1-assess-charter.md` — where this inventory runs.
- `../governance-as-code/councils/` — the new charter this inventory is
  checked against.
- `offering-overview.md` — "What's In Scope" lists this alongside
  organizational design.
