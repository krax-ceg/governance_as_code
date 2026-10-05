#!/usr/bin/env python3
"""Group one or more generated ODCS data contracts into an ODPS (Open Data
Product Standard) product descriptor.

Usage:
    python generate_odps_product.py \\
        --contract data_contract_factory_lead_times.yaml \\
        --product-name "Supplier Lead Time Performance" \\
        --owner-name "Jane Doe" --owner-email "jane.doe@enterprise.com" \\
        --platform databricks --location "main.procurement_gold.factory_lead_times" \\
        --out data_product.yaml

Accepts one or more --contract flags to group multiple contracts into a
single product (one outputPort per contract).
"""
import argparse

import yaml


def build_product(contracts: list[dict], product_name: str, owner: dict,
                   platform: str, locations: list[str], tier: str = "gold") -> dict:
    if len(locations) not in (1, len(contracts)):
        raise ValueError("--location must be given once, or once per --contract")
    if len(locations) == 1:
        locations = locations * len(contracts)

    domain = contracts[0]["accountability"]["domain"]
    slug = product_name.lower().replace(" ", "_")

    output_ports = []
    sla_refs = []
    for contract, location in zip(contracts, locations):
        contract_id = contract["metadata"]["id"]
        asset_name = contract_id.rsplit(":", 1)[-1]
        output_ports.append({
            "id": f"{asset_name}_{tier}",
            "name": asset_name.replace("_", " ").title(),
            "contractId": contract_id,
            "type": "table",
            "platform": platform,
            "location": location,
        })
        if "service_level_agreement" in contract:
            sla_refs.append(f"{contract_id}#service_level_agreement")

    product = {
        "apiVersion": "bitol.io/odps/v1alpha1",
        "kind": "DataProduct",
        "id": f"urn:ent:domain:{domain}:dataproduct:{slug}",
        "name": product_name,
        "status": "draft",
        "version": "0.1.0",
        "domain": domain,
        "tier": tier,
        "owner": owner,
        "outputPorts": output_ports,
    }
    if sla_refs:
        product["slaRefs"] = sla_refs
    support_channel = contracts[0]["accountability"].get("support_channel")
    if support_channel:
        product["supportChannel"] = support_channel

    return product


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", action="append", required=True, dest="contracts",
                         help="Path to a generated ODCS contract YAML (repeatable)")
    parser.add_argument("--product-name", required=True)
    parser.add_argument("--owner-name", required=True)
    parser.add_argument("--owner-email", required=True)
    parser.add_argument("--platform", required=True, choices=["databricks", "fabric", "snowflake", "other"])
    parser.add_argument("--location", action="append", required=True,
                         help="Platform-native locator; repeat once per --contract, or pass once for all")
    parser.add_argument("--tier", default="gold", choices=["bronze", "gold", "platinum"])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    contracts = []
    for path in args.contracts:
        with open(path) as f:
            contracts.append(yaml.safe_load(f))

    product = build_product(
        contracts,
        product_name=args.product_name,
        owner={"name": args.owner_name, "email": args.owner_email},
        platform=args.platform,
        locations=args.location,
        tier=args.tier,
    )

    with open(args.out, "w") as f:
        yaml.dump(product, f, sort_keys=False, default_flow_style=False)

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
