#!/usr/bin/env python3
"""Validate atomic task backlog files under tasks/*/backlog.yaml."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

TASK_ID_PATTERN = re.compile(r"^SS-\d{3}$")
ALLOWED_STATUS = {"todo", "in_progress", "done", "blocked"}
ALLOWED_PRIORITY = {"P0", "P1", "P2"}
REQUIRED_ROOT_KEYS = {"version", "board", "repo", "updated_at", "tasks"}
REQUIRED_TASK_KEYS = {
    "id",
    "status",
    "priority",
    "title",
    "objective",
    "atomic_change",
    "file_scope",
    "done_when",
    "depends_on",
}


@dataclass
class IssueBag:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def load_yaml(path: Path, issues: IssueBag) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        issues.add_error(f"{path}: failed to parse YAML ({exc})")
        return None

    if not isinstance(data, dict):
        issues.add_error(f"{path}: root must be a mapping")
        return None
    return data


def validate_string_list(
    value: Any, field_name: str, location: str, issues: IssueBag, *, allow_empty: bool = False
) -> list[str]:
    if not isinstance(value, list):
        issues.add_error(f"{location}: {field_name} must be a list")
        return []

    cleaned: list[str] = []
    for index, item in enumerate(value):
        text = str(item).strip()
        if not text:
            issues.add_error(f"{location}: {field_name}[{index}] must be non-empty")
            continue
        cleaned.append(text)

    if not allow_empty and not cleaned:
        issues.add_error(f"{location}: {field_name} must not be empty")
    return cleaned


def validate_backlog(path: Path, issues: IssueBag) -> int:
    data = load_yaml(path, issues)
    if data is None:
        return 0

    missing_root_keys = sorted(REQUIRED_ROOT_KEYS - data.keys())
    if missing_root_keys:
        issues.add_error(f"{path}: missing root keys -> {', '.join(missing_root_keys)}")

    tasks_value = data.get("tasks")
    if not isinstance(tasks_value, list):
        issues.add_error(f"{path}: tasks must be a list")
        return 0
    if not tasks_value:
        issues.add_error(f"{path}: tasks must contain at least one task")
        return 0

    task_count = 0
    in_progress_count = 0
    task_ids: set[str] = set()
    task_dependencies: list[tuple[str, str, list[str]]] = []

    for index, raw_task in enumerate(tasks_value):
        task_count += 1
        location = f"{path}:tasks[{index}]"

        if not isinstance(raw_task, dict):
            issues.add_error(f"{location}: task must be a mapping")
            continue

        missing_task_keys = sorted(REQUIRED_TASK_KEYS - raw_task.keys())
        if missing_task_keys:
            issues.add_error(
                f"{location}: missing task keys -> {', '.join(missing_task_keys)}"
            )

        task_id = str(raw_task.get("id", "")).strip()
        if not TASK_ID_PATTERN.match(task_id):
            issues.add_error(f"{location}: id must match pattern SS-000")
        elif task_id in task_ids:
            issues.add_error(f"{location}: duplicate task id -> {task_id}")
        else:
            task_ids.add(task_id)

        status = str(raw_task.get("status", "")).strip()
        if status not in ALLOWED_STATUS:
            issues.add_error(
                f"{location}: status must be one of {sorted(ALLOWED_STATUS)}"
            )
        if status == "in_progress":
            in_progress_count += 1

        priority = str(raw_task.get("priority", "")).strip()
        if priority not in ALLOWED_PRIORITY:
            issues.add_error(
                f"{location}: priority must be one of {sorted(ALLOWED_PRIORITY)}"
            )

        for key in ("title", "objective", "atomic_change"):
            value = str(raw_task.get(key, "")).strip()
            if not value:
                issues.add_error(f"{location}: {key} must be non-empty")

        validate_string_list(raw_task.get("file_scope"), "file_scope", location, issues)
        validate_string_list(raw_task.get("done_when"), "done_when", location, issues)
        depends_on = validate_string_list(
            raw_task.get("depends_on"), "depends_on", location, issues, allow_empty=True
        )

        if task_id:
            task_dependencies.append((task_id, location, depends_on))

    if in_progress_count > 1:
        issues.add_error(
            f"{path}: at most one task can be in_progress (found {in_progress_count})"
        )

    for task_id, location, dependencies in task_dependencies:
        for dependency_id in dependencies:
            if dependency_id == task_id:
                issues.add_error(f"{location}: depends_on must not include self -> {task_id}")
                continue
            if dependency_id not in task_ids:
                issues.add_error(
                    f"{location}: depends_on references unknown task id -> {dependency_id}"
                )

    return task_count


def resolve_backlog_paths(repo_root: Path, cli_paths: list[str]) -> list[Path]:
    if cli_paths:
        resolved_paths: list[Path] = []
        for raw_path in cli_paths:
            path = Path(raw_path)
            if not path.is_absolute():
                path = (repo_root / path).resolve()
            resolved_paths.append(path)
        return resolved_paths

    return sorted((repo_root / "tasks").glob("*/backlog.yaml"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate task backlog YAML definitions.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional backlog file paths. Defaults to tasks/*/backlog.yaml.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    backlog_paths = resolve_backlog_paths(repo_root, args.paths)

    if not backlog_paths:
        print("No backlog files found under tasks/*/backlog.yaml", file=sys.stderr)
        return 1

    issues = IssueBag()
    total_tasks = 0

    for backlog_path in backlog_paths:
        if not backlog_path.exists():
            issues.add_error(f"{backlog_path}: file not found")
            continue
        total_tasks += validate_backlog(backlog_path, issues)

    if issues.warnings:
        print("Backlog validation warnings:")
        for warning in issues.warnings:
            print(f"- {warning}")

    if issues.errors:
        print("Backlog validation failed:", file=sys.stderr)
        for err in issues.errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(backlog_paths)} backlog file(s), {total_tasks} task(s) total"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
