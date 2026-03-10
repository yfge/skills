# PR Audit Example

## Input

- Pull request diff affecting multiple skills.
- Policy: blocker-first, minimal-file edits.

## Expected Output

- Delta-focused blocker and suggestion list.
- File-level remediation actions.
- Post-fix regression status.

## Acceptance Notes

- Scope remains constrained to changed files where possible.
- High-risk regressions are explicitly flagged.
- Remaining debt is queued with priority.
