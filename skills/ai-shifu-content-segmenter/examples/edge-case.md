# Edge Case Example

## Input

- Multiple source files with partial overlap.
- Missing heading hierarchy.
- Broken narrative sequence.

## Expected Output

- Coarse but stable segmentation with uncertainty markers.
- Preserved immutable blocks.
- Re-run hints for affected lesson spans.

## Acceptance Notes

- Fallback path is explicit.
- Uncertain spans are flagged, not silently rewritten.
- Downstream skills can consume the output without schema changes.
