# Skill Stability Atomic Iterations (v2)

This board focuses on turning `ai-shifu-skills` into an indexable, forwardable, reusable, and searchable product catalog.

## Focus Axes

1. Indexability: structured metadata can be exported reliably.
2. Forwardability: each skill has concise handoff-ready descriptors.
3. Reusability: input/output contracts are explicit and verifiable.
4. Searchability: query intent fields are complete and validated.

## Principles

1. One task = one smallest safe change.
2. Each task must be independently verifiable.
3. Run regression commands after each task.
4. Keep repository and skill slugs unchanged (`ai-shifu-skills`).

## Regression Commands

```bash
python3 scripts/validate_task_backlog.py
python3 scripts/validate_openai_yaml.py
python3 scripts/validate_skill_quality.py
python3 scripts/build_catalog.py
python3 scripts/build_quality_report.py
```

## Status Model

- `todo`: not started
- `in_progress`: currently being implemented
- `done`: merged and verified
- `blocked`: waiting on dependency/decision

## Execution Rule

1. Pick the highest-priority `todo` task with dependencies satisfied.
2. Move to `in_progress`.
3. Implement only the declared file scope.
4. Run regression commands.
5. Move to `done` if acceptance checks pass.
