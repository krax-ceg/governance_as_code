package gac.data_contracts.validation

import future.keywords.if

test_valid_payload if {
	valid with input as {
		"contract": {
			"required_fields": ["po_id", "amount"],
			"field_types": {"po_id": "string", "amount": "number"},
			"strict": false,
		},
		"payload": {"po_id": "PO-123", "amount": 42.5},
	}
}

test_invalid_missing_field if {
	not valid with input as {
		"contract": {
			"required_fields": ["po_id", "amount"],
			"field_types": {"po_id": "string", "amount": "number"},
			"strict": false,
		},
		"payload": {"po_id": "PO-123"},
	}
}

test_invalid_wrong_type if {
	not valid with input as {
		"contract": {
			"required_fields": ["po_id", "amount"],
			"field_types": {"po_id": "string", "amount": "number"},
			"strict": false,
		},
		"payload": {"po_id": "PO-123", "amount": "not-a-number"},
	}
}

test_invalid_strict_unexpected_field if {
	not valid with input as {
		"contract": {
			"required_fields": ["po_id"],
			"field_types": {"po_id": "string"},
			"strict": true,
		},
		"payload": {"po_id": "PO-123", "extra_field": "nope"},
	}
}
