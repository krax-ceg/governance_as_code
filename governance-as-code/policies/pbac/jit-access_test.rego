package gac.pbac.jit

import future.keywords.if

test_valid_grant if {
	valid with input as {
		"now": 100,
		"grant": {
			"request_status": "approved",
			"granted_at": 0,
			"expires_at": 500,
			"requested_resources": ["table_a"],
			"approved_resources": ["table_a", "table_b"],
		},
	}
}

test_invalid_expired_grant if {
	not valid with input as {
		"now": 1000,
		"grant": {
			"request_status": "approved",
			"granted_at": 0,
			"expires_at": 500,
			"requested_resources": ["table_a"],
			"approved_resources": ["table_a"],
		},
	}
}

test_invalid_scope_exceeds_approved if {
	not valid with input as {
		"now": 100,
		"grant": {
			"request_status": "approved",
			"granted_at": 0,
			"expires_at": 500,
			"requested_resources": ["table_a", "table_c"],
			"approved_resources": ["table_a"],
		},
	}
}

test_invalid_not_approved if {
	not valid with input as {
		"now": 100,
		"grant": {
			"request_status": "pending",
			"granted_at": 0,
			"expires_at": 500,
			"requested_resources": ["table_a"],
			"approved_resources": ["table_a"],
		},
	}
}
