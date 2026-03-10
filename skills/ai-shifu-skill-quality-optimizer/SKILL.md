---
name: ai-shifu-skill-quality-optimizer
description: Audits and improves skill repository quality with issue severity grading, minimal safe remediation, and regression validation.
---

# Skill Quality Optimizer

Govern quality across `skills/` with a structured loop: baseline -> triage -> minimal remediation -> regression.

## Minimum Inputs

- Repository path (current repository by default).
- Scope (single skill or full repository).
- Optional constraints (blockers only, include suggestions, edit-scope limits).

## Workflow

1. Run baseline commands:
- `python3 scripts/validate_openai_yaml.py`
- `python3 scripts/validate_skill_quality.py`
- `python3 scripts/build_catalog.py`
- `python3 scripts/build_quality_report.py`

2. Classify findings from `quality/quality-report.md` and `quality/quality-summary.json`:
- `blocker`: breaks validation or functional usability; must be fixed.
- `suggestion`: non-blocking quality debt impacting discoverability or maintainability.

3. Apply minimal remediation using `references/remediation-playbook.md`:
- Fix blockers first.
- Restrict edits to issue-related files.
- Re-run regression immediately after each fix.

4. Produce change and validation summary:
- Edited file list.
- Resolution status by issue class.
- Remaining suggestions with next-priority recommendations.

## Output Requirements

- Start with repository quality status: `pass` or `blocked`.
- Then list fixes grouped by `blocker` and `suggestion`.
- Include traceable file references.
- Include regression command results.

## Quality Gate

- Blocker count must be zero for a passing state.
- Every new skill must include:
- `SKILL.md`
- `agents/openai.yaml`
- `skill.yaml`
- `examples/` (at least one example)
- Valid `demo` field and reachable `demo.url` path when `repo_example` is used.

See `references/quality-rubric.md` for scoring criteria.
See `references/remediation-playbook.md` for common fix strategies.

## Validation Checkpoints

- Status (`pass|blocked`) is reported first.
- Blockers and suggestions are grouped by priority with file-level traceability.
- Remediation stays within minimal safe scope.
- Regression command outcomes are attached.
- Task board and iteration logs are updated when workflow changes.

## Report Template

See `references/report-template.md`.

## Related Skills

- Governance target: `ai-shifu-content-segmenter`
- Governance target: `ai-shifu-transcript-to-lessons`
- Governance target: `ai-shifu-lesson-script-generator`
- Governance target: `ai-shifu-lesson-script-optimizer`

## Examples

- `examples/minimal.md`
- `examples/pr-audit.md`
