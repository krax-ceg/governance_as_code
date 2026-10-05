package gac.pbac.jit

import future.keywords.if

# Just-in-Time (JIT) access policy — replaces standing RBAC grants with
# time-limited, task-specific credentials (Phase 3, Days 71-80).
# A JIT grant is valid only if it has an approved request, has not expired,
# and the requested scope does not exceed the approved scope.

default valid := false

valid if {
	input.grant.request_status == "approved"
	not expired
	scope_within_approved
}

expired if {
	input.grant.expires_at <= input.now
}

scope_within_approved if {
	every r in input.grant.requested_resources {
		r in input.grant.approved_resources
	}
}

# Maximum grant duration allowed without re-approval, in seconds (8 hours).
max_grant_duration_seconds := 28800

violates_max_duration if {
	(input.grant.expires_at - input.grant.granted_at) > max_grant_duration_seconds
}

deny_reason contains "grant not approved" if {
	input.grant.request_status != "approved"
}

deny_reason contains "grant expired" if {
	expired
}

deny_reason contains "requested scope exceeds approved scope" if {
	not scope_within_approved
}

deny_reason contains "grant duration exceeds policy maximum" if {
	violates_max_duration
}
