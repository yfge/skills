#!/usr/bin/env python3
"""Validate skills/*/agents/openai.yaml for interface metadata consistency."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_INTERFACE_FIELDS = ["display_name", "short_description", "default_prompt"]


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return raw


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = load_yaml(path)
    except ValueError as exc:
        return [str(exc)]

    interface = data.get("interface")
    if not isinstance(interface, dict):
        return [f"{path}: top-level key 'interface' must exist and be a mapping"]

    for field in REQUIRED_INTERFACE_FIELDS:
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: interface.{field} must be a non-empty string")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    yaml_files = sorted(repo_root.glob("skills/*/agents/openai.yaml"))
    if not yaml_files:
        print("No agents/openai.yaml found under skills/", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for yaml_file in yaml_files:
        all_errors.extend(validate_file(yaml_file))

    if all_errors:
        print("OpenAI metadata validation failed:", file=sys.stderr)
        for err in all_errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(f"Validated {len(yaml_files)} openai.yaml files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
