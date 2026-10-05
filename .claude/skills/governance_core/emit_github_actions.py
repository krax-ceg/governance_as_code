#!/usr/bin/env python3
"""Render the GitHub Actions governance-validation workflow into a target
repo's .github/workflows/ directory.

Usage:
    python emit_github_actions.py --target-repo /path/to/client/repo \\
        [--contracts-dir governance-as-code/contracts] \\
        [--products-dir governance-as-code/contracts]
"""
import argparse
import os

from jinja2 import Template

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-repo", required=True, help="Root of the client repo to write into")
    parser.add_argument("--contracts-dir", default="governance-as-code/contracts")
    parser.add_argument("--products-dir", default="governance-as-code/contracts")
    args = parser.parse_args()

    template_path = os.path.join(_SCRIPT_DIR, "templates", "github_actions_governance.yml.j2")
    with open(template_path) as f:
        template = Template(f.read())

    rendered = template.render(contracts_dir=args.contracts_dir, products_dir=args.products_dir)

    out_dir = os.path.join(args.target_repo, ".github", "workflows")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "governance-as-code.yml")
    with open(out_path, "w") as f:
        f.write(rendered)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
