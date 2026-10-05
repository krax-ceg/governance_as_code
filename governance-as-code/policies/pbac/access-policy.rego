package gac.pbac.access

import future.keywords.in
import future.keywords.if

# Reference Policy-Based Access Control (PBAC) policy.
# Replaces static RBAC groups (Phase 2 baseline) with attribute/policy-driven
# decisions evaluated per-request. Customize `allowed_sensitivity_for_role`
# and `domain_match` for the client's actual role and domain taxonomy.

default allow := false

# Allow if the requester's role is cleared for the dataset's sensitivity
# tier AND the requester belongs to the dataset's owning domain (or is a
# member of the Central Hub, which can read across domains for audit).
allow if {
	input.action == "read"
	allowed_sensitivity_for_role[input.subject.role][input.resource.sensitivity]
	domain_match
}

domain_match if {
	input.subject.domain == input.resource.domain
}

domain_match if {
	input.subject.role == "hub_auditor"
}

# Role -> set of sensitivity tiers that role may read.
allowed_sensitivity_for_role := {
	"domain_business_owner": {"public", "internal", "confidential"},
	"data_steward": {"public", "internal", "confidential"},
	"data_engineer": {"public", "internal"},
	"hub_auditor": {"public", "internal", "confidential", "restricted"},
	"general_user": {"public"},
}

# Deny reasons surfaced to the caller for audit logging.
deny_reason contains msg if {
	not allow
	not domain_match
	msg := sprintf("subject domain '%v' does not match resource domain '%v'", [input.subject.domain, input.resource.domain])
}

deny_reason contains msg if {
	not allow
	domain_match
	not allowed_sensitivity_for_role[input.subject.role][input.resource.sensitivity]
	msg := sprintf("role '%v' is not cleared for sensitivity tier '%v'", [input.subject.role, input.resource.sensitivity])
}
