#!/usr/bin/env python3
"""Detect which CI system a target repo should get governance validation
wired into, based on its git remote.

Usage:
    python detect_git_remote.py [--repo PATH]

Prints one of: github, azure-devops, unknown
Exits non-zero only on an unexpected error — "unknown" is a normal, valid
result (e.g. no remote configured yet) and exits 0.
"""
import argparse
import subprocess
import sys


def detect(repo_path: str = ".") -> str:
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10,
        )
    except FileNotFoundError:
        print("ERROR: git is not installed or not on PATH", file=sys.stderr)
        sys.exit(2)

    if result.returncode != 0:
        # No remote configured, or not a git repo at all -- both are
        # "unknown", not an error: the skill should fall back to asking
        # the operator which CI system to scaffold for.
        return "unknown"

    url = result.stdout.strip().lower()
    if "github.com" in url:
        return "github"
    if "dev.azure.com" in url or "visualstudio.com" in url:
        return "azure-devops"
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Path to the target repo (default: current directory)")
    args = parser.parse_args()
    print(detect(args.repo))


if __name__ == "__main__":
    main()
