#!/usr/bin/env python3
"""Bridge a generated ODCS data contract into the `input.contract` shape
expected by ../../governance-as-code/policies/data-contracts/contract-validation.rego.

The schema-registry policy was written against a simplified internal shape
(required_fields / field_types / strict) that predates the ODCS layer added
by the Databricks/Fabric onboarding skills. Rather than rewrite the
already-tested Rego policy (and its _test.rego suite), this script maps
ODCS -> that shape so the two layers interoperate without duplicating
validation logic.

Usage:
    python odcs_to_policy_input.py --contract data_contract.yaml --out policy_input.json
    opa eval -i policy_input.json -d ../../governance-as-code/policies/data-contracts/contract-validation.rego \\
        'data.gac.data_contracts.validation.valid'
"""
import argparse
import json

import yaml

_ODCS_TO_REGO_TYPE = {
    "string": "string",
    "number": "number",
    "boolean": "boolean",
}


def convert(contract: dict) -> dict:
    schema = contract["schema"]
    return {
        "required_fields": schema["required"],
        "field_types": {
            name: _ODCS_TO_REGO_TYPE.get(prop.get("type", "string"), "string")
            for name, prop in schema["properties"].items()
        },
        "strict": not schema.get("additionalProperties", True),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, help="Path to an ODCS contract YAML")
    parser.add_argument("--out", required=True, help="Output path for the Rego-ready policy input JSON")
    args = parser.parse_args()

    with open(args.contract) as f:
        contract = yaml.safe_load(f)

    policy_contract = convert(contract)
    with open(args.out, "w") as f:
        json.dump({"contract": policy_contract}, f, indent=2)

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
