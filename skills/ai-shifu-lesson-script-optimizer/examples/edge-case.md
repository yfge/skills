# Edge Case Example

## Input Payload (example)

```json
{
  "existing_mdf_script": "## Goal\nPick a fix.\n---\n?[%{{fix_choice}} option A | option B]\n---\n?[%{{choose_fix}} option A | option B]\n---\nUse {{unknown_variable}} now.",
  "source_course_material": "",
  "optimization_constraints": {
    "fallback_mode": true,
    "minimize_scope": true
  },
  "delivery_constraints": {
    "platform_limits": ["markdown_only"]
  }
}
```

## Output Snapshot (example)

```json
{
  "risk_and_issue_report": {
    "overall_risk": "high",
    "blocking_issues": [
      "variable_or_syntax_risk",
      "semantic_duplicate_interactions"
    ],
    "coverage_status": "unknown_without_source"
  },
  "change_list": [
    {
      "issue_class": "variable_or_syntax_risk",
      "change": "remove unknown variable reference and keep one canonical interaction variable"
    }
  ],
  "follow_up": [
    "Provide source material for full coverage and meaning audit."
  ]
}
```

```md
## Goal
Pick one safe first fix.
---
?[%{{fix_choice}} option A | option B]
---
You selected {{fix_choice}}. Apply one verification step before rollout.
```

## Acceptance Notes

- Runtime safety fixes are applied first.
- Missing-source uncertainty is explicit in the report.
- Edits stay minimal and avoid broad rewrites.
