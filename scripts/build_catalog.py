#!/usr/bin/env python3
"""Build catalog artifacts from skills/*/skill.yaml.

Outputs:
  - catalog/skills.json
  - catalog/skills.csv
  - INDEX.md
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FIELDS = [
    "schema_version",
    "name",
    "slug",
    "one_liner",
    "description",
    "category",
    "target_users",
    "primary_problem",
    "inputs",
    "outputs",
    "maturity",
    "reusability_score",
    "docs_score",
    "keywords",
    "triggers",
    "related_skills",
    "owner",
    "license",
    "last_verified_at",
]

CSV_COLUMNS = [
    "slug",
    "name",
    "one_liner",
    "category",
    "maturity",
    "target_users",
    "primary_problem",
    "inputs",
    "outputs",
    "internal_skills",
    "external_services",
    "api_keys_required",
    "reusability_score",
    "docs_score",
    "demo_type",
    "demo_url",
    "keywords_zh",
    "keywords_en",
    "triggers_zh",
    "triggers_en",
    "related_skills",
    "aliases_zh",
    "aliases_en",
    "owner",
    "license",
    "last_verified_at",
    "skill_path",
]


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return raw


def parse_frontmatter(skill_md: Path) -> dict[str, Any]:
    if not skill_md.exists():
        return {}

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    parsed = yaml.safe_load(parts[1]) or {}
    return parsed if isinstance(parsed, dict) else {}


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def join_list(value: Any) -> str:
    return ";".join(str(item).strip() for item in ensure_list(value) if str(item).strip())


def flatten_io(value: Any) -> str:
    items = ensure_list(value)
    flattened: list[str] = []
    for item in items:
        if isinstance(item, dict):
            name = str(item.get("name", "")).strip()
            item_type = str(item.get("type", "")).strip()
            required = item.get("required", "")
            if name or item_type:
                flattened.append(f"{name}:{item_type}:{required}")
        else:
            flattened.append(str(item))
    return ";".join(flattened)


def rel_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def merge_skill_data(
    skill_dir: Path, skill_data: dict[str, Any], repo_root: Path
) -> dict[str, Any]:
    frontmatter = parse_frontmatter(skill_dir / "SKILL.md")

    merged = dict(skill_data)
    merged.setdefault("name", frontmatter.get("name", skill_dir.name))
    merged.setdefault("slug", skill_dir.name)
    merged.setdefault("description", frontmatter.get("description", ""))

    merged["target_users"] = ensure_list(merged.get("target_users"))
    merged["inputs"] = ensure_list(merged.get("inputs"))
    merged["outputs"] = ensure_list(merged.get("outputs"))

    keywords = merged.get("keywords")
    if not isinstance(keywords, dict):
        keywords = {"zh": [], "en": []}
    keywords["zh"] = ensure_list(keywords.get("zh"))
    keywords["en"] = ensure_list(keywords.get("en"))
    merged["keywords"] = keywords

    triggers = merged.get("triggers")
    if not isinstance(triggers, dict):
        triggers = {"zh": [], "en": []}
    triggers["zh"] = ensure_list(triggers.get("zh"))
    triggers["en"] = ensure_list(triggers.get("en"))
    merged["triggers"] = triggers

    merged["related_skills"] = ensure_list(merged.get("related_skills"))

    aliases = merged.get("aliases")
    if not isinstance(aliases, dict):
        aliases = {"zh": [], "en": []}
    aliases["zh"] = ensure_list(aliases.get("zh"))
    aliases["en"] = ensure_list(aliases.get("en"))
    merged["aliases"] = aliases

    dependencies = merged.get("dependencies")
    if not isinstance(dependencies, dict):
        dependencies = {}
    dependencies["internal_skills"] = ensure_list(dependencies.get("internal_skills"))
    dependencies["external_services"] = ensure_list(dependencies.get("external_services"))
    dependencies["api_keys_required"] = bool(dependencies.get("api_keys_required", False))
    merged["dependencies"] = dependencies

    demo = merged.get("demo")
    if not isinstance(demo, dict):
        demo = {"type": "none", "url": ""}
    demo.setdefault("type", "none")
    demo.setdefault("url", "")
    merged["demo"] = demo

    merged["skill_path"] = rel_path(skill_dir, repo_root)
    merged["skill_md_path"] = rel_path(skill_dir / "SKILL.md", repo_root)
    merged["openai_yaml_path"] = rel_path(skill_dir / "agents" / "openai.yaml", repo_root)
    return merged


def validate_skill(skill: dict[str, Any], source_file: Path) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in skill:
            errors.append(f"{source_file}: missing required field '{field}'")

    slug = str(skill.get("slug", "")).strip()
    if not slug:
        errors.append(f"{source_file}: 'slug' must not be empty")

    for field in ("target_users", "inputs", "outputs"):
        if not isinstance(skill.get(field), list):
            errors.append(f"{source_file}: '{field}' must be a list")

    triggers = skill.get("triggers", {})
    if not isinstance(triggers, dict):
        errors.append(f"{source_file}: 'triggers' must be a mapping")
    else:
        for lang in ("zh", "en"):
            values = triggers.get(lang)
            if not isinstance(values, list):
                errors.append(f"{source_file}: triggers.{lang} must be a list")
                continue
            clean_values = [str(item).strip() for item in values if str(item).strip()]
            if len(clean_values) < 3:
                errors.append(
                    f"{source_file}: triggers.{lang} requires at least 3 non-empty entries"
                )

    related_skills = skill.get("related_skills")
    if not isinstance(related_skills, list):
        errors.append(f"{source_file}: 'related_skills' must be a list")

    for field in ("reusability_score", "docs_score"):
        value = skill.get(field)
        if not isinstance(value, int):
            errors.append(f"{source_file}: '{field}' must be an integer")
            continue
        if value < 0 or value > 5:
            errors.append(f"{source_file}: '{field}' must be between 0 and 5")

    if skill.get("maturity") not in {"experimental", "beta", "stable", "deprecated"}:
        errors.append(
            f"{source_file}: 'maturity' must be one of experimental|beta|stable|deprecated"
        )
    return errors


def to_csv_row(skill: dict[str, Any]) -> dict[str, str]:
    deps = skill.get("dependencies", {})
    demo = skill.get("demo", {})
    keywords = skill.get("keywords", {})
    triggers = skill.get("triggers", {})
    aliases = skill.get("aliases", {})

    return {
        "slug": str(skill.get("slug", "")),
        "name": str(skill.get("name", "")),
        "one_liner": str(skill.get("one_liner", "")),
        "category": str(skill.get("category", "")),
        "maturity": str(skill.get("maturity", "")),
        "target_users": join_list(skill.get("target_users")),
        "primary_problem": str(skill.get("primary_problem", "")),
        "inputs": flatten_io(skill.get("inputs")),
        "outputs": flatten_io(skill.get("outputs")),
        "internal_skills": join_list(deps.get("internal_skills")),
        "external_services": join_list(deps.get("external_services")),
        "api_keys_required": str(bool(deps.get("api_keys_required", False))).lower(),
        "reusability_score": str(skill.get("reusability_score", "")),
        "docs_score": str(skill.get("docs_score", "")),
        "demo_type": str(demo.get("type", "")),
        "demo_url": str(demo.get("url", "")),
        "keywords_zh": join_list(keywords.get("zh")),
        "keywords_en": join_list(keywords.get("en")),
        "triggers_zh": join_list(triggers.get("zh")),
        "triggers_en": join_list(triggers.get("en")),
        "related_skills": join_list(skill.get("related_skills")),
        "aliases_zh": join_list(aliases.get("zh")),
        "aliases_en": join_list(aliases.get("en")),
        "owner": str(skill.get("owner", "")),
        "license": str(skill.get("license", "")),
        "last_verified_at": str(skill.get("last_verified_at", "")),
        "skill_path": str(skill.get("skill_path", "")),
    }


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def generate_index(catalog: list[dict[str, Any]], index_path: Path) -> None:
    lines: list[str] = []
    lines.append("# Skill Index")
    lines.append("")
    lines.append("<!-- AUTO-GENERATED by scripts/build_catalog.py. DO NOT EDIT MANUALLY. -->")
    lines.append("")
    lines.append(f"Total skills: **{len(catalog)}**")
    lines.append("")
    lines.append("| Skill | One-liner | Category | Maturity |")
    lines.append("|---|---|---|---|")
    for skill in catalog:
        name = md_escape(str(skill.get("name", "")))
        one_liner = md_escape(str(skill.get("one_liner", "")))
        category = md_escape(str(skill.get("category", "")))
        maturity = md_escape(str(skill.get("maturity", "")))
        skill_md_path = str(skill.get("skill_md_path", ""))
        lines.append(f"| [{name}](./{skill_md_path}) | {one_liner} | {category} | {maturity} |")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")


def build_catalog(
    skills_dir: Path, catalog_dir: Path, index_path: Path, include_generated_at: bool
) -> int:
    skill_yaml_files = sorted(skills_dir.glob("*/skill.yaml"))
    if not skill_yaml_files:
        print(f"No skill.yaml found under {skills_dir}", file=sys.stderr)
        return 1

    repo_root = skills_dir.parent
    catalog: list[dict[str, Any]] = []
    errors: list[str] = []
    seen_slugs: set[str] = set()

    for skill_yaml_file in skill_yaml_files:
        skill_dir = skill_yaml_file.parent
        try:
            raw = load_yaml(skill_yaml_file)
            merged = merge_skill_data(skill_dir, raw, repo_root)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        errors.extend(validate_skill(merged, skill_yaml_file))

        slug = str(merged.get("slug", "")).strip()
        if slug in seen_slugs:
            errors.append(f"{skill_yaml_file}: duplicate slug '{slug}'")
        seen_slugs.add(slug)
        catalog.append(merged)

    if errors:
        print("Catalog build failed with validation errors:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    catalog.sort(key=lambda item: str(item.get("slug", "")))
    catalog_dir.mkdir(parents=True, exist_ok=True)

    json_path = catalog_dir / "skills.json"
    json_payload = {"total_skills": len(catalog), "skills": catalog}
    if include_generated_at:
        from datetime import datetime

        json_payload["generated_at"] = (
            datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        )
    json_path.write_text(
        json.dumps(json_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    csv_path = catalog_dir / "skills.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for skill in catalog:
            writer.writerow(to_csv_row(skill))

    generate_index(catalog, index_path)

    print(f"Built {len(catalog)} skills")
    print(f"- {json_path}")
    print(f"- {csv_path}")
    print(f"- {index_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build catalog artifacts from skills/*/skill.yaml"
    )
    parser.add_argument(
        "--skills-dir",
        default="skills",
        help="Path to skills directory (default: skills)",
    )
    parser.add_argument(
        "--catalog-dir",
        default="catalog",
        help="Path to output catalog directory (default: catalog)",
    )
    parser.add_argument(
        "--include-generated-at",
        action="store_true",
        help="Include volatile generated_at timestamp in JSON output",
    )
    parser.add_argument(
        "--index-path",
        default="INDEX.md",
        help="Path to generated index markdown (default: INDEX.md)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skills_dir = Path(args.skills_dir).resolve()
    catalog_dir = Path(args.catalog_dir).resolve()
    index_path = Path(args.index_path).resolve()
    return build_catalog(skills_dir, catalog_dir, index_path, args.include_generated_at)


if __name__ == "__main__":
    raise SystemExit(main())
