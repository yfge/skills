#!/usr/bin/env python3
"""Build skill quality report artifacts.

Outputs:
  - quality/quality-report.md
  - quality/quality-summary.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

MATURITY_SET = {"experimental", "beta", "stable", "deprecated"}
RE_REF_PATH = re.compile(r"references/[A-Za-z0-9_./-]+\.md")


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class SkillReport:
    slug: str
    maturity: str
    docs_score: int
    reusability_score: int
    blocker_checks: list[CheckResult]
    suggestion_checks: list[CheckResult]
    example_count: int
    demo_url: str

    @property
    def blockers_passed(self) -> int:
        return sum(1 for c in self.blocker_checks if c.passed)

    @property
    def blockers_total(self) -> int:
        return len(self.blocker_checks)

    @property
    def suggestions_passed(self) -> int:
        return sum(1 for c in self.suggestion_checks if c.passed)

    @property
    def suggestions_total(self) -> int:
        return len(self.suggestion_checks)

    @property
    def blocker_ratio(self) -> float:
        return self.blockers_passed / self.blockers_total if self.blockers_total else 0.0

    @property
    def suggestion_ratio(self) -> float:
        return self.suggestions_passed / self.suggestions_total if self.suggestions_total else 0.0

    @property
    def quality_score(self) -> float:
        # 70% blocker checks + 20% suggestion checks + 10% declared rubric quality.
        rubric_docs = max(self.docs_score, 0)
        rubric_reuse = max(self.reusability_score, 0)
        rubric_ratio = (rubric_docs + rubric_reuse) / 10.0
        return round((self.blocker_ratio * 70.0) + (self.suggestion_ratio * 20.0) + (rubric_ratio * 10.0), 1)

    @property
    def status(self) -> str:
        if self.failed_blockers:
            return "blocked"
        score = self.quality_score
        if score >= 90:
            return "excellent"
        if score >= 75:
            return "good"
        return "attention"

    @property
    def failed_blockers(self) -> list[CheckResult]:
        return [c for c in self.blocker_checks if not c.passed]

    @property
    def failed_suggestions(self) -> list[CheckResult]:
        return [c for c in self.suggestion_checks if not c.passed]


def load_yaml(path: Path) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    return data if isinstance(data, dict) else None


def parse_frontmatter(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception:  # noqa: BLE001
        return None
    return data if isinstance(data, dict) else None


def check_true(name: str, condition: bool, detail: str = "") -> CheckResult:
    return CheckResult(name=name, passed=condition, detail=detail)


def build_skill_report(skill_dir: Path, repo_root: Path) -> SkillReport:
    slug = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    skill_yaml_path = skill_dir / "skill.yaml"
    openai_yaml_path = skill_dir / "agents" / "openai.yaml"
    examples_dir = skill_dir / "examples"

    frontmatter = parse_frontmatter(skill_md) or {}
    skill_yaml = load_yaml(skill_yaml_path) or {}
    openai_yaml = load_yaml(openai_yaml_path) or {}
    interface = openai_yaml.get("interface") if isinstance(openai_yaml.get("interface"), dict) else {}

    examples = sorted(examples_dir.glob("*.md")) if examples_dir.exists() else []
    example_count = len(examples)

    missing_refs: list[str] = []
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8")
        refs = sorted(set(RE_REF_PATH.findall(content)))
        for ref in refs:
            if not (skill_dir / ref).exists():
                missing_refs.append(ref)
    else:
        missing_refs.append("SKILL.md missing")

    demo = skill_yaml.get("demo") if isinstance(skill_yaml.get("demo"), dict) else {}
    demo_type = str(demo.get("type", "")).strip()
    demo_url = str(demo.get("url", "")).strip()
    demo_path_ok = True
    if demo_type == "repo_example":
        if not demo_url:
            demo_path_ok = False
        else:
            demo_path_ok = (repo_root / demo_url.removeprefix("./")).exists()

    docs_score = skill_yaml.get("docs_score")
    reuse_score = skill_yaml.get("reusability_score")
    docs_score = docs_score if isinstance(docs_score, int) else -1
    reuse_score = reuse_score if isinstance(reuse_score, int) else -1

    short_description = str(interface.get("short_description", "")).strip()
    default_prompt = str(interface.get("default_prompt", "")).strip()

    keywords = skill_yaml.get("keywords") if isinstance(skill_yaml.get("keywords"), dict) else {}
    keywords_zh = keywords.get("zh") if isinstance(keywords.get("zh"), list) else []
    keywords_en = keywords.get("en") if isinstance(keywords.get("en"), list) else []

    blocker_checks = [
        check_true("has_skill_md", skill_md.exists()),
        check_true("has_skill_yaml", skill_yaml_path.exists()),
        check_true("has_openai_yaml", openai_yaml_path.exists()),
        check_true("frontmatter_name_matches_slug", frontmatter.get("name") == slug),
        check_true(
            "frontmatter_has_description",
            isinstance(frontmatter.get("description"), str)
            and bool(str(frontmatter.get("description", "")).strip()),
        ),
        check_true("skill_yaml_name_matches_slug", skill_yaml.get("name") == slug),
        check_true("skill_yaml_slug_matches_folder", skill_yaml.get("slug") == slug),
        check_true("maturity_is_valid", skill_yaml.get("maturity") in MATURITY_SET),
        check_true("has_examples", example_count > 0, f"examples_found={example_count}"),
        check_true("demo_path_is_valid", demo_path_ok, f"demo_url={demo_url}"),
        check_true(
            "openai_interface_complete",
            all(
                isinstance(interface.get(key), str) and bool(str(interface.get(key)).strip())
                for key in ("display_name", "short_description", "default_prompt")
            ),
        ),
        check_true(
            "default_prompt_contains_skill_reference",
            isinstance(interface.get("default_prompt"), str) and f"${slug}" in str(interface.get("default_prompt", "")),
        ),
        check_true("all_references_exist", len(missing_refs) == 0, ";".join(missing_refs)),
    ]

    suggestion_checks = [
        check_true(
            "short_description_length_recommended",
            20 <= len(short_description) <= 80,
            f"len={len(short_description)}",
        ),
        check_true(
            "default_prompt_length_recommended",
            20 <= len(default_prompt) <= 180,
            f"len={len(default_prompt)}",
        ),
        check_true(
            "example_count_recommended",
            example_count >= 2,
            f"examples_found={example_count}",
        ),
        check_true("docs_score_recommended", docs_score >= 4, f"docs_score={docs_score}"),
        check_true("reusability_score_recommended", reuse_score >= 4, f"reusability_score={reuse_score}"),
        check_true("keywords_zh_recommended", len(keywords_zh) >= 3, f"keywords_zh={len(keywords_zh)}"),
        check_true("keywords_en_recommended", len(keywords_en) >= 3, f"keywords_en={len(keywords_en)}"),
    ]

    maturity = str(skill_yaml.get("maturity", "unknown"))
    return SkillReport(
        slug=slug,
        maturity=maturity,
        docs_score=docs_score,
        reusability_score=reuse_score,
        blocker_checks=blocker_checks,
        suggestion_checks=suggestion_checks,
        example_count=example_count,
        demo_url=demo_url,
    )


def render_report(reports: list[SkillReport]) -> str:
    total = len(reports)
    blockers_failed_skills = sum(1 for report in reports if report.failed_blockers)
    suggestions_failed_total = sum(len(report.failed_suggestions) for report in reports)
    avg_score = round(sum(report.quality_score for report in reports) / total, 1) if total else 0.0

    lines: list[str] = []
    lines.append("# Skill Quality Report")
    lines.append("")
    lines.append("<!-- AUTO-GENERATED by scripts/build_quality_report.py. DO NOT EDIT MANUALLY. -->")
    lines.append("")
    lines.append(f"- Total skills: **{total}**")
    lines.append(f"- Skills with blocker issues: **{blockers_failed_skills}/{total}**")
    lines.append(f"- Total suggestion issues: **{suggestions_failed_total}**")
    lines.append(f"- Average quality score: **{avg_score} / 100**")
    lines.append("")
    lines.append("| Skill | Score | Status | Blockers | Suggestions | Maturity | Docs | Reuse | Examples |")
    lines.append("|---|---:|---|---:|---:|---|---:|---:|---:|")

    for report in reports:
        lines.append(
            f"| `{report.slug}` | {report.quality_score} | {report.status} | "
            f"{report.blockers_passed}/{report.blockers_total} | {report.suggestions_passed}/{report.suggestions_total} | "
            f"{report.maturity} | {report.docs_score} | {report.reusability_score} | {report.example_count} |"
        )

    lines.append("")
    lines.append("## Blockers (Must Fix)")
    lines.append("")
    blocker_any = False
    for report in reports:
        if not report.failed_blockers:
            continue
        blocker_any = True
        lines.append(f"### {report.slug}")
        for check in report.failed_blockers:
            detail = f" ({check.detail})" if check.detail else ""
            lines.append(f"- `{check.name}`{detail}")
        lines.append("")
    if not blocker_any:
        lines.append("- None")
        lines.append("")

    lines.append("## Suggestions (Should Improve)")
    lines.append("")
    suggestion_any = False
    for report in reports:
        if not report.failed_suggestions:
            continue
        suggestion_any = True
        lines.append(f"### {report.slug}")
        for check in report.failed_suggestions:
            detail = f" ({check.detail})" if check.detail else ""
            lines.append(f"- `{check.name}`{detail}")
        lines.append("")
    if not suggestion_any:
        lines.append("- None")
        lines.append("")

    return "\n".join(lines)


def build_summary(reports: list[SkillReport]) -> dict[str, Any]:
    blockers_failed_skills = sum(1 for report in reports if report.failed_blockers)
    suggestions_failed_total = sum(len(report.failed_suggestions) for report in reports)
    avg_score = round(sum(report.quality_score for report in reports) / len(reports), 1) if reports else 0.0

    overall_status = "pass" if blockers_failed_skills == 0 else "blocked"
    return {
        "total_skills": len(reports),
        "skills_with_blockers": blockers_failed_skills,
        "suggestion_issues_total": suggestions_failed_total,
        "average_quality_score": avg_score,
        "overall_status": overall_status,
        "skills": [
            {
                "slug": report.slug,
                "quality_score": report.quality_score,
                "status": report.status,
                "maturity": report.maturity,
                "docs_score": report.docs_score,
                "reusability_score": report.reusability_score,
                "example_count": report.example_count,
                "blockers": [
                    {"name": check.name, "detail": check.detail}
                    for check in report.failed_blockers
                ],
                "suggestions": [
                    {"name": check.name, "detail": check.detail}
                    for check in report.failed_suggestions
                ],
            }
            for report in reports
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build skill quality markdown/json reports")
    parser.add_argument("--skills-dir", default="skills", help="Path to skills directory")
    parser.add_argument(
        "--output",
        default="quality/quality-report.md",
        help="Path to output quality markdown report",
    )
    parser.add_argument(
        "--summary-output",
        default="quality/quality-summary.json",
        help="Path to output quality summary json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skills_dir = Path(args.skills_dir).resolve()
    repo_root = skills_dir.parent
    output = Path(args.output).resolve()
    summary_output = Path(args.summary_output).resolve()

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    reports = [build_skill_report(skill_dir, repo_root) for skill_dir in skill_dirs]

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(reports) + "\n", encoding="utf-8")
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.write_text(
        json.dumps(build_summary(reports), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Built quality report for {len(reports)} skills")
    print(f"- {output}")
    print(f"- {summary_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
