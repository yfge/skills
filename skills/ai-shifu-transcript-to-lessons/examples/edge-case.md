# Edge Case Example

## Input

- Multiple partially overlapping documents.
- Missing section hierarchy.
- Contradictory terminology across files.

## Expected Output

- Coarse lesson drafts with explicit uncertainty markers.
- Partial index and variable table with rerun annotations.
- Clear rerun scope for affected lessons only.

## Acceptance Notes

- Pipeline does not fail hard.
- Uncertain parts are transparent.
- Downstream optimization can proceed incrementally.
