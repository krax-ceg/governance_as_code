#!/usr/bin/env python3
"""Generate an ODCS (Open Data Contract Standard) data contract YAML from an
introspected table payload plus Core-10 operator-supplied metadata.

Shared by governance-onboard-databricks and governance-onboard-fabric — do
not duplicate this logic per-platform; introspection connectors produce a
common JSON shape (see `INTROSPECTED_TABLE_SHAPE` below) that this module
consumes identically regardless of source platform.

Usage:
    python generate_odcs_contract.py \\
        --table introspected_table.json \\
        --operator-input operator_input.json \\
        --out data_contract.yaml

introspected_table.json (produced by a platform connector):
    {
      "domain": "procurement",
      "asset_name": "factory_lead_times",
      "source_system_id": "sys_databricks_uc",
      "data_residency_region": "eu-central-1",
      "columns": [
        {"name": "purchase_order_id", "type": "string", "nullable": false},
        {"name": "calculated_lead_time_days", "type": "double", "nullable": false}
      ]
    }

operator_input.json (the five Core-10 fields no platform API can tell you):
    {
      "data_owner": {"name": "...", "email": "..."},
      "data_steward": {"name": "...", "email": "..."},
      "classification": "restricted",
      "criticality": "tier-1",
      "support_channel": "#help-procurement-data"
    }
"""
import argparse
import json
import sys
from datetime import date

import yaml

# Minimal platform-type -> JSON Schema type mapping. Extend as new platform
# connectors are added; keep it a flat dict so it stays a one-line diff.
_TYPE_MAP = {
    "string": "string",
    "varchar": "string",
    "int": "number",
    "integer": "number",
    "bigint": "number",
    "double": "number",
    "float": "number",
    "decimal": "number",
    "boolean": "boolean",
    "timestamp": "string",
    "date": "string",
}

REQUIRED_OPERATOR_FIELDS = [
    "data_owner",
    "data_steward",
    "classification",
    "criticality",
    "support_channel",
]


def _json_type(platform_type: str) -> str:
    return _TYPE_MAP.get(platform_type.lower(), "string")


def build_contract(table: dict, operator_input: dict, version: str = "0.1.0") -> dict:
    missing = [f for f in REQUIRED_OPERATOR_FIELDS if f not in operator_input]
    if missing:
        raise ValueError(
            f"operator input is missing Core-10 fields that cannot be introspected: {missing}. "
            "See governance-as-code/schemas/core10-and-31-attribute-framework.md."
        )

    domain = table["domain"]
    asset_name = table["asset_name"]
    required_cols = [c["name"] for c in table["columns"] if not c.get("nullable", True)]
    properties = {
        c["name"]: {"type": _json_type(c["type"])} for c in table["columns"]
    }

    contract = {
        "apiVersion": "bitol.io/odcs/v1alpha1",
        "kind": "DataContract",
        "metadata": {
            "id": f"urn:ent:domain:{domain}:product:{asset_name}",
            "version": version,
            "status": "draft",
        },
        "accountability": {
            "domain": domain,
            "data_owner": operator_input["data_owner"],
            "data_steward": operator_input["data_steward"],
            "classification": operator_input["classification"],
            "criticality": operator_input["criticality"],
            "support_channel": operator_input["support_channel"],
        },
        "lifecycle": {
            "effective_from": date.today().isoformat(),
        },
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": required_cols,
            "properties": properties,
        },
    }

    if table.get("source_system_id"):
        contract["metadata"]["source_system_id"] = table["source_system_id"]
    if table.get("data_residency_region"):
        contract["metadata"]["data_residency_region"] = table["data_residency_region"]

    return contract


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True, help="Path to an introspected-table JSON file")
    parser.add_argument("--operator-input", required=True, help="Path to a Core-10 operator-input JSON file")
    parser.add_argument("--version", default="0.1.0", help="Initial contract SemVer (default: 0.1.0)")
    parser.add_argument("--out", required=True, help="Output path for the generated ODCS YAML")
    args = parser.parse_args()

    with open(args.table) as f:
        table = json.load(f)
    with open(args.operator_input) as f:
        operator_input = json.load(f)

    try:
        contract = build_contract(table, operator_input, version=args.version)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    with open(args.out, "w") as f:
        yaml.dump(contract, f, sort_keys=False, default_flow_style=False)

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
