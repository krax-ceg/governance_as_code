package gac.pbac.access

import future.keywords.if

test_allow_steward_same_domain_confidential if {
	allow with input as {
		"action": "read",
		"subject": {"role": "data_steward", "domain": "procurement"},
		"resource": {"domain": "procurement", "sensitivity": "confidential"},
	}
}

test_deny_cross_domain if {
	not allow with input as {
		"action": "read",
		"subject": {"role": "data_steward", "domain": "procurement"},
		"resource": {"domain": "manufacturing", "sensitivity": "internal"},
	}
}

test_allow_hub_auditor_cross_domain if {
	allow with input as {
		"action": "read",
		"subject": {"role": "hub_auditor", "domain": "hub"},
		"resource": {"domain": "manufacturing", "sensitivity": "restricted"},
	}
}

test_deny_general_user_confidential if {
	not allow with input as {
		"action": "read",
		"subject": {"role": "general_user", "domain": "procurement"},
		"resource": {"domain": "procurement", "sensitivity": "confidential"},
	}
}
