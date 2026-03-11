# Remediation Playbook

## Blocker-First Strategy

1. Reproduce with baseline commands.
2. Isolate minimal file scope.
3. Apply smallest safe fix.
4. Re-run regression immediately.
5. Document result and residual risk.

## Common Fix Patterns

- Missing metadata fields: add required keys with valid values.
- Broken references: update paths or add missing files.
- Invalid prompt metadata: fix interface fields and skill reference token.
- Artifact drift: rebuild catalog and quality outputs.

## Change Control Rules

- Avoid unrelated refactors in the same patch.
- Keep path-level traceability for each fix.
- Do not downgrade strictness to pass checks.
