#!/usr/bin/env python3
"""Validate cross-file quality for all skills."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

RE_REF_PATH = re.compile(r"references/[A-Za-z0-9_./-]+\.md")
MATURITY_SET = {"experimental", "beta", "stable", "deprecated"}
RE_HAN = re.compile(r"[\u4e00-\u9fff]")
CORE_LANGUAGE_SKILLS = {
    "ai-shifu-content-segmenter",
    "ai-shifu-transcript-to-lessons",
    "ai-shifu-lesson-script-generator",
    "ai-shifu-lesson-script-optimizer",
}
LANGUAGE_PRIORITY = [
    "explicit_output_language_request",
    "target_language_parameter",
    "session_language_preference",
    "prompt_language_detection",
    "source_material_dominant_language",
    "default_fallback_language",
]
LANGUAGE_INPUT_TYPES = {
    "target_language": "text",
    "bilingual_output": "boolean",
    "term_policy": "text",
    "quote_policy": "text",
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
        issues.add_error(f"{path}: YAML root must be a mapping")
        return None
    return data


def parse_skill_frontmatter(skill_md: Path, issues: IssueBag) -> dict[str, Any] | None:
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        issues.add_error(f"{skill_md}: missing YAML frontmatter")
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.add_error(f"{skill_md}: malformed YAML frontmatter")
        return None
    try:
        front = yaml.safe_load(parts[1]) or {}
    except Exception as exc:  # noqa: BLE001
        issues.add_error(f"{skill_md}: invalid frontmatter YAML ({exc})")
        return None
    if not isinstance(front, dict):
        issues.add_error(f"{skill_md}: frontmatter must be a mapping")
        return None
    return front


def validate_references(skill_dir: Path, skill_md: Path, issues: IssueBag) -> None:
    content = skill_md.read_text(encoding="utf-8")
    ref_paths = sorted(set(RE_REF_PATH.findall(content)))
    for ref in ref_paths:
        ref_file = skill_dir / ref
        if not ref_file.exists():
            issues.add_error(f"{skill_md}: referenced file not found -> {ref}")


def validate_english_only(skill_dir: Path, issues: IssueBag) -> None:
    english_required_files: list[Path] = [
        skill_dir / "SKILL.md",
        skill_dir / "skill.yaml",
        skill_dir / "agents" / "openai.yaml",
    ]
    english_required_files.extend(sorted((skill_dir / "examples").glob("*.md")))
    english_required_files.extend(sorted((skill_dir / "references").glob("*.md")))

    for file_path in english_required_files:
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8")
        if RE_HAN.search(content):
            issues.add_error(
                f"{file_path}: contains Han-script characters; skill artifacts must be authored in English"
            )


def validate_language_contract(
    slug: str,
    skill_md: Path,
    skill_yaml_file: Path,
    skill_yaml: dict[str, Any],
    issues: IssueBag,
) -> None:
    if slug not in CORE_LANGUAGE_SKILLS:
        return

    inputs = skill_yaml.get("inputs")
    input_map: dict[str, dict[str, Any]] = {}
    if not isinstance(inputs, list):
        issues.add_error(
            f"{skill_yaml_file}: inputs must be a list to validate language controls"
        )
    else:
        for idx, item in enumerate(inputs):
            if not isinstance(item, dict):
                issues.add_error(f"{skill_yaml_file}: inputs[{idx}] must be a mapping")
                continue
            input_name = str(item.get("name", "")).strip()
            if not input_name:
                issues.add_error(
                    f"{skill_yaml_file}: inputs[{idx}].name must be non-empty"
                )
                continue
            input_map[input_name] = item

    for field_name, expected_type in LANGUAGE_INPUT_TYPES.items():
        field = input_map.get(field_name)
        if field is None:
            issues.add_error(
                f"{skill_yaml_file}: missing language-control input '{field_name}'"
            )
            continue
        field_type = str(field.get("type", "")).strip()
        if expected_type not in field_type:
            issues.add_error(
                f"{skill_yaml_file}: input '{field_name}' must include type '{expected_type}'"
            )

    language_resolution = skill_yaml.get("language_resolution")
    if not isinstance(language_resolution, dict):
        issues.add_error(
            f"{skill_yaml_file}: language_resolution mapping is required for core multilingual skills"
        )
    else:
        if language_resolution.get("allow_any_language") is not True:
            issues.add_error(
                f"{skill_yaml_file}: language_resolution.allow_any_language must be true"
            )
        if not isinstance(language_resolution.get("bcp47_recommended"), bool):
            issues.add_error(
                f"{skill_yaml_file}: language_resolution.bcp47_recommended must be boolean"
            )
        fallback_language = str(
            language_resolution.get("default_fallback_language", "")
        ).strip()
        if not fallback_language:
            issues.add_error(
                f"{skill_yaml_file}: language_resolution.default_fallback_language must be non-empty"
            )
        priority = language_resolution.get("priority")
        if not isinstance(priority, list):
            issues.add_error(
                f"{skill_yaml_file}: language_resolution.priority must be a list"
            )
        else:
            normalized_priority = [str(item).strip() for item in priority]
            if normalized_priority != LANGUAGE_PRIORITY:
                issues.add_error(
                    f"{skill_yaml_file}: language_resolution.priority must match {LANGUAGE_PRIORITY}"
                )

    skill_content = skill_md.read_text(encoding="utf-8")
    if "## Language Resolution Policy" not in skill_content:
        issues.add_error(
            f"{skill_md}: missing '## Language Resolution Policy' section"
        )
    for marker in LANGUAGE_PRIORITY:
        if marker not in skill_content:
            issues.add_error(
                f"{skill_md}: Language Resolution Policy missing '{marker}' marker"
            )
    for marker in LANGUAGE_INPUT_TYPES:
        if marker not in skill_content:
            issues.add_error(
                f"{skill_md}: Language Resolution Policy missing '{marker}' field reference"
            )


def validate_skill(
    skill_dir: Path, repo_root: Path, known_slugs: set[str], issues: IssueBag
) -> None:
    slug = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    skill_yaml_file = skill_dir / "skill.yaml"
    openai_yaml_file = skill_dir / "agents" / "openai.yaml"
    examples_dir = skill_dir / "examples"

    for file_path in (skill_md, skill_yaml_file, openai_yaml_file):
        if not file_path.exists():
            issues.add_error(f"{skill_dir}: required file missing -> {file_path.name}")
            return

    front = parse_skill_frontmatter(skill_md, issues)
    skill_yaml = load_yaml(skill_yaml_file, issues)
    openai_yaml = load_yaml(openai_yaml_file, issues)
    if front is None or skill_yaml is None or openai_yaml is None:
        return

    if front.get("name") != slug:
        issues.add_error(f"{skill_md}: frontmatter name must match folder slug '{slug}'")
    if not isinstance(front.get("description"), str) or not front.get("description", "").strip():
        issues.add_error(f"{skill_md}: frontmatter description must be non-empty")

    if skill_yaml.get("name") != slug:
        issues.add_error(f"{skill_yaml_file}: name must match slug '{slug}'")
    if skill_yaml.get("slug") != slug:
        issues.add_error(f"{skill_yaml_file}: slug must match folder slug '{slug}'")
    if skill_yaml.get("maturity") not in MATURITY_SET:
        issues.add_error(
            f"{skill_yaml_file}: maturity must be one of {sorted(MATURITY_SET)}"
        )

    for score_key in ("reusability_score", "docs_score"):
        value = skill_yaml.get(score_key)
        if not isinstance(value, int) or value < 0 or value > 5:
            issues.add_error(f"{skill_yaml_file}: {score_key} must be an integer in [0, 5]")

    triggers = skill_yaml.get("triggers")
    if not isinstance(triggers, dict):
        issues.add_error(f"{skill_yaml_file}: triggers must be a mapping with zh/en lists")
    else:
        for lang in ("zh", "en"):
            values = triggers.get(lang)
            if not isinstance(values, list):
                issues.add_error(f"{skill_yaml_file}: triggers.{lang} must be a list")
                continue
            clean_values = [str(item).strip() for item in values if str(item).strip()]
            if len(clean_values) < 3:
                issues.add_error(
                    f"{skill_yaml_file}: triggers.{lang} requires at least 3 non-empty entries"
                )

    related_skills = skill_yaml.get("related_skills")
    if not isinstance(related_skills, list):
        issues.add_error(f"{skill_yaml_file}: related_skills must be a list")
    else:
        for related in related_skills:
            related_slug = str(related).strip()
            if not related_slug:
                issues.add_error(f"{skill_yaml_file}: related_skills contains empty value")
                continue
            if related_slug == slug:
                issues.add_warning(
                    f"{skill_yaml_file}: related_skills contains self reference '{slug}'"
                )
            if related_slug not in known_slugs:
                issues.add_error(
                    f"{skill_yaml_file}: related skill slug not found -> {related_slug}"
                )

    demo = skill_yaml.get("demo", {})
    if not isinstance(demo, dict):
        issues.add_error(f"{skill_yaml_file}: demo must be a mapping")
    else:
        demo_type = demo.get("type")
        demo_url = str(demo.get("url", "")).strip()
        if demo_type == "repo_example":
            if not demo_url:
                issues.add_error(f"{skill_yaml_file}: demo.url is required for repo_example")
            else:
                demo_path = (repo_root / demo_url.removeprefix("./")).resolve()
                if not demo_path.exists():
                    issues.add_error(
                        f"{skill_yaml_file}: demo.url path not found -> {demo_url}"
                    )

    if not examples_dir.exists():
        issues.add_error(f"{skill_dir}: examples directory is required")
    else:
        example_files = list(examples_dir.glob("*.md"))
        if not example_files:
            issues.add_error(f"{examples_dir}: at least one markdown example is required")

    interface = openai_yaml.get("interface")
    if not isinstance(interface, dict):
        issues.add_error(f"{openai_yaml_file}: top-level 'interface' mapping is required")
    else:
        for key in ("display_name", "short_description", "default_prompt"):
            value = interface.get(key)
            if not isinstance(value, str) or not value.strip():
                issues.add_error(f"{openai_yaml_file}: interface.{key} must be non-empty")
        short_desc = str(interface.get("short_description", "")).strip()
        if short_desc and not (20 <= len(short_desc) <= 80):
            issues.add_warning(
                f"{openai_yaml_file}: short_description length is {len(short_desc)} "
                "(recommended 20-80 chars)"
            )
        default_prompt = str(interface.get("default_prompt", "")).strip()
        if default_prompt and f"${slug}" not in default_prompt:
            issues.add_error(
                f"{openai_yaml_file}: interface.default_prompt must include ${slug}"
            )

    validate_references(skill_dir, skill_md, issues)
    validate_english_only(skill_dir, issues)
    validate_language_contract(slug, skill_md, skill_yaml_file, skill_yaml, issues)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skills_root = repo_root / "skills"
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    known_slugs = {path.name for path in skill_dirs}

    if not skill_dirs:
        print("No skills found under skills/", file=sys.stderr)
        return 1

    issues = IssueBag()
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, repo_root, known_slugs, issues)

    if issues.warnings:
        print("Skill quality warnings:")
        for warning in issues.warnings:
            print(f"- {warning}")

    if issues.errors:
        print("Skill quality validation failed:", file=sys.stderr)
        for err in issues.errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(f"Validated skill quality for {len(skill_dirs)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
