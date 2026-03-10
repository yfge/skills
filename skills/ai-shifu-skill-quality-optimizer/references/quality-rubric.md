# Quality Rubric

## Scoring Dimensions

1. Structural completeness
- Required files exist.
- Required metadata fields are present and valid.

2. Execution safety
- Prompt interface metadata is valid.
- Variable and reference rules are enforced.

3. Discoverability
- Triggers, keywords, and related-skill links are complete.
- Catalog exports are up to date.

4. Maintainability
- Examples exist and remain representative.
- Documentation supports repeatable operation.

## Severity Definitions

- Blocker: Validation failure or functional failure.
- Suggestion: Non-blocking quality debt or maintainability gap.

## Pass Criteria

- Blocker count = 0.
- Regression commands succeed.
- Generated artifacts are committed and in sync.
