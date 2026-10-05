package gac.data_contracts.validation

import future.keywords.if
import future.keywords.in

# Schema registry validation policy (Phase 3, Days 61-70).
# Rejects event payloads that violate the declared data contract: missing
# required fields, wrong types, or unknown fields when the contract is strict.

default valid := false

valid if {
	required_fields_present
	no_type_violations
	no_unexpected_fields
}

required_fields_present if {
	every f in input.contract.required_fields {
		f in object.keys(input.payload)
	}
}

no_type_violations if {
	every field_name, expected_type in input.contract.field_types {
		type_matches(field_name, expected_type)
	}
}

type_matches(field_name, expected_type) if {
	not field_name in object.keys(input.payload)
}

type_matches(field_name, expected_type) if {
	value := input.payload[field_name]
	expected_type == "string"
	is_string(value)
}

type_matches(field_name, expected_type) if {
	value := input.payload[field_name]
	expected_type == "number"
	is_number(value)
}

type_matches(field_name, expected_type) if {
	value := input.payload[field_name]
	expected_type == "boolean"
	is_boolean(value)
}

no_unexpected_fields if {
	not input.contract.strict
}

no_unexpected_fields if {
	input.contract.strict
	every k in object.keys(input.payload) {
		k in input.contract.required_fields
	}
}

violation contains msg if {
	not required_fields_present
	missing := [f | some f in input.contract.required_fields; not f in object.keys(input.payload)]
	msg := sprintf("missing required fields: %v", [missing])
}

violation contains msg if {
	not no_type_violations
	msg := "one or more fields do not match the contract's declared type"
}

violation contains msg if {
	not no_unexpected_fields
	msg := "payload contains fields not declared in a strict contract"
}
