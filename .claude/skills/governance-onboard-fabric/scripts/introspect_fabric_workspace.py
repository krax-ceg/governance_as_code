#!/usr/bin/env python3
"""Read-only introspection of a Microsoft Fabric lakehouse, producing the
common `introspected_table.json` shape consumed by
../../governance_core/generate_odcs_contract.py.

Credentials: an Azure AD bearer token with Fabric API read scope, supplied
via the FABRIC_TOKEN environment variable (e.g. obtained with
`az account get-access-token --resource https://api.fabric.microsoft.com`
and exported by the caller — this script never runs that command itself or
reads an Azure CLI session, to keep its credential surface to one env var).
Never pass the token on the command line.

This script only issues GET requests against the Fabric REST API
(workspaces, items, and lakehouse table/column metadata). It does not
create, modify, or assign any workspace roles or sensitivity labels — see
SKILL.md for why that's a deliberate scope boundary for the first release.

Usage:
    python introspect_fabric_workspace.py \\
        --workspace-id <workspace_guid> --lakehouse-id <lakehouse_guid> \\
        --table factory_lead_times \\
        --out introspected_table.json

    # Or introspect every table in the lakehouse at once:
    python introspect_fabric_workspace.py \\
        --workspace-id <workspace_guid> --lakehouse-id <lakehouse_guid> \\
        --all-tables --out-dir introspected/
"""
import argparse
import json
import os
import sys

_FABRIC_API_BASE = "https://api.fabric.microsoft.com/v1"


def _get_session():
    try:
        import requests
    except ImportError:
        print("ERROR: the 'requests' package is required (pip install requests).", file=sys.stderr)
        sys.exit(2)

    token = os.environ.get("FABRIC_TOKEN")
    if not token:
        print(
            "ERROR: FABRIC_TOKEN must be set in the environment to a valid "
            "Azure AD bearer token for the Fabric API. Credentials are never "
            "read from command-line flags.",
            file=sys.stderr,
        )
        sys.exit(2)

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session


# Fabric/Delta type names -> the shared shape's lowercase type vocabulary.
_FABRIC_TYPE_MAP = {
    "string": "string",
    "long": "bigint",
    "integer": "int",
    "double": "double",
    "float": "float",
    "boolean": "boolean",
    "timestamp": "timestamp",
    "date": "date",
}


def _list_table_names(session, workspace_id: str, lakehouse_id: str) -> list[str]:
    """Read-only: GET /workspaces/{id}/lakehouses/{id}/tables."""
    resp = session.get(
        f"{_FABRIC_API_BASE}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables",
        timeout=30,
    )
    resp.raise_for_status()
    return [t["name"] for t in resp.json().get("data", [])]


def introspect_table(session, workspace_id: str, lakehouse_id: str, table_name: str) -> dict:
    """Read-only: GET the table's schema via the Fabric SQL endpoint's
    information_schema-equivalent, or the table-load metadata endpoint,
    depending on workspace configuration. Column introspection detail is
    workspace-specific; this wraps whatever the enabled Fabric API surface
    returns into the shared shape."""
    resp = session.get(
        f"{_FABRIC_API_BASE}/workspaces/{workspace_id}/lakehouses/{lakehouse_id}/tables/{table_name}",
        timeout=30,
    )
    resp.raise_for_status()
    table_meta = resp.json()

    columns = []
    for col in table_meta.get("schema", {}).get("columns", []):
        columns.append({
            "name": col["name"],
            "type": _FABRIC_TYPE_MAP.get(col.get("type", "string").lower(), "string"),
            "nullable": col.get("nullable", True),
        })

    return {
        "domain": table_meta.get("schema", {}).get("defaultSchema", "unknown"),
        "asset_name": table_name,
        "source_system_id": f"sys_fabric_lakehouse_{lakehouse_id}",
        "data_residency_region": None,  # set manually from the workspace's capacity region if required
        "columns": columns,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-id", required=True)
    parser.add_argument("--lakehouse-id", required=True)
    parser.add_argument("--table", help="Single table to introspect")
    parser.add_argument("--all-tables", action="store_true", help="Introspect every table in the lakehouse")
    parser.add_argument("--out", help="Output path (single-table mode)")
    parser.add_argument("--out-dir", help="Output directory (--all-tables mode)")
    args = parser.parse_args()

    if not args.table and not args.all_tables:
        parser.error("specify --table <name> or --all-tables")
    if args.table and not args.out:
        parser.error("--table requires --out")
    if args.all_tables and not args.out_dir:
        parser.error("--all-tables requires --out-dir")

    session = _get_session()

    if args.table:
        payload = introspect_table(session, args.workspace_id, args.lakehouse_id, args.table)
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote {args.out}")
    else:
        os.makedirs(args.out_dir, exist_ok=True)
        for table_name in _list_table_names(session, args.workspace_id, args.lakehouse_id):
            payload = introspect_table(session, args.workspace_id, args.lakehouse_id, table_name)
            out_path = os.path.join(args.out_dir, f"{table_name}.json")
            with open(out_path, "w") as f:
                json.dump(payload, f, indent=2)
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
