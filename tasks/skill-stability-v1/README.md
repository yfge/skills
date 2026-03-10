# Skill Stability Atomic Iterations (v1)

This task board defines minimal atomic iterations for improving `ai-shifu-skills` quality and stability.

## Principles

1. One task = one smallest safe change.
2. Each task must be independently verifiable.
3. Always run regression commands after each task.
4. Do not rename repository or existing skill slugs.

## Regression Commands

```bash
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

1. Pick the highest-priority `todo` task with all dependencies satisfied.
2. Move to `in_progress`.
3. Implement only the declared file scope.
4. Run regression commands.
5. Move to `done` if all acceptance checks pass.
