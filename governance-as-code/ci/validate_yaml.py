#!/usr/bin/env python3
"""Validate one or more YAML files against a JSON Schema."""
import argparse
import json
import sys

import yaml
from jsonschema import Draft7Validator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    with open(args.schema) as f:
        schema = json.load(f)
    validator = Draft7Validator(schema)

    exit_code = 0
    for path in args.files:
        with open(path) as f:
            doc = yaml.safe_load(f)
        errors = sorted(validator.iter_errors(doc), key=lambda e: e.path)
        if errors:
            exit_code = 1
            print(f"FAIL: {path}")
            for e in errors:
                loc = "/".join(str(p) for p in e.path) or "<root>"
                print(f"  - {loc}: {e.message}")
        else:
            print(f"OK:   {path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
