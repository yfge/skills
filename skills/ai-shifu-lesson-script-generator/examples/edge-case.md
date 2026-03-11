# Edge Case Example

## Input Payload (example)

```json
{
  "structured_lesson_segments": [
    {
      "lesson_id": "L07",
      "core_question": "What is the safest rollback trigger?",
      "segment_ids": ["S70"]
    }
  ],
  "teaching_constraints": {
    "max_interactions": 2,
    "must_use_viewpoint_check": true,
    "allow_cross_lesson_dependency": false
  },
  "delivery_constraints": {
    "platform_limits": ["markdown_only"]
  }
}
```

## Output Snapshot (example)

```json
{
  "lesson_id": "L07",
  "fallback_mode": true,
  "assumptions": [
    "No cross-lesson variable carryover is used.",
    "One viewpoint check is enough for this pass."
  ],
  "upgrade_notes": [
    "Add richer evidence chain after full source context is available."
  ]
}
```

```md
## Objective
Pick a rollback trigger that minimizes blast radius.
---
?[%{{rollback_trigger_viewpoint_check}} latency spike threshold | error budget burn threshold]
---
Given {{rollback_trigger_viewpoint_check}}, define one immediate rollback condition and one follow-up diagnostic.
```

## Acceptance Notes

- Script remains valid in fallback mode.
- Interaction count stays within declared limits.
- Output stays concrete and learner-facing.
