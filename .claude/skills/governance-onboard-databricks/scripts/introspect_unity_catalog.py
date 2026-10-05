#!/usr/bin/env python3
"""Read-only introspection of a Databricks Unity Catalog schema, producing
the common `introspected_table.json` shape consumed by
../../governance_core/generate_odcs_contract.py.

Credentials: standard Databricks auth env vars — DATABRICKS_HOST and
DATABRICKS_TOKEN (or any auth method the Databricks SDK supports, e.g. a
~/.databrickscfg profile via --profile). Never pass tokens on the command
line.

This script only ever calls read endpoints (information_schema SELECTs via
the SQL Statement Execution API, or GET on /api/2.1/unity-catalog/*). It does
not create, alter, or grant anything in Unity Catalog — see SKILL.md for why
that's a deliberate scope boundary for the first release.

Usage:
    python introspect_unity_catalog.py \\
        --catalog main --schema procurement_bronze --table factory_lead_times \\
        --warehouse-id <sql_warehouse_id> \\
        --out introspected_table.json

    # Or introspect every table in a schema at once:
    python introspect_unity_catalog.py \\
        --catalog main --schema procurement_bronze --all-tables \\
        --warehouse-id <sql_warehouse_id> \\
        --out-dir introspected/
"""
import argparse
import json
import os
import sys


def _get_workspace_client():
    try:
        from databricks.sdk import WorkspaceClient
    except ImportError:
        print(
            "ERROR: the 'databricks-sdk' package is required "
            "(pip install databricks-sdk).",
            file=sys.stderr,
        )
        sys.exit(2)

    if not os.environ.get("DATABRICKS_HOST") or not os.environ.get("DATABRICKS_TOKEN"):
        print(
            "ERROR: DATABRICKS_HOST and DATABRICKS_TOKEN must be set in the "
            "environment (or configure a ~/.databrickscfg profile and pass "
            "--profile). Credentials are never read from command-line flags.",
            file=sys.stderr,
        )
        sys.exit(2)

    return WorkspaceClient()


def introspect_table(client, catalog: str, schema: str, table: str) -> dict:
    """Read-only: GET /api/2.1/unity-catalog/tables/{full_name}."""
    full_name = f"{catalog}.{schema}.{table}"
    t = client.tables.get(full_name=full_name)

    columns = []
    for col in t.columns or []:
        columns.append({
            "name": col.name,
            "type": (col.type_name.value if col.type_name else "string").lower(),
            "nullable": bool(col.nullable) if col.nullable is not None else True,
        })

    return {
        "domain": schema.replace("_bronze", "").replace("_gold", ""),
        "asset_name": table,
        "source_system_id": f"sys_databricks_uc_{catalog}",
        "data_residency_region": None,  # not exposed by Unity Catalog metadata; set manually if required
        "columns": columns,
    }


def list_tables(client, catalog: str, schema: str) -> list[str]:
    """Read-only: GET /api/2.1/unity-catalog/tables (list)."""
    return [t.name for t in client.tables.list(catalog_name=catalog, schema_name=schema)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--table", help="Single table to introspect")
    parser.add_argument("--all-tables", action="store_true", help="Introspect every table in --schema")
    parser.add_argument("--warehouse-id", help="Reserved for future statement-execution-API fallback; unused by the SDK table-metadata path")
    parser.add_argument("--out", help="Output path (single-table mode)")
    parser.add_argument("--out-dir", help="Output directory (--all-tables mode)")
    args = parser.parse_args()

    if not args.table and not args.all_tables:
        parser.error("specify --table <name> or --all-tables")
    if args.table and not args.out:
        parser.error("--table requires --out")
    if args.all_tables and not args.out_dir:
        parser.error("--all-tables requires --out-dir")

    client = _get_workspace_client()

    if args.table:
        payload = introspect_table(client, args.catalog, args.schema, args.table)
        with open(args.out, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote {args.out}")
    else:
        os.makedirs(args.out_dir, exist_ok=True)
        for table_name in list_tables(client, args.catalog, args.schema):
            payload = introspect_table(client, args.catalog, args.schema, table_name)
            out_path = os.path.join(args.out_dir, f"{table_name}.json")
            with open(out_path, "w") as f:
                json.dump(payload, f, indent=2)
            print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
