# Minimal Example

## Input Payload (example)

```json
{
  "structured_lesson_segments": [
    {
      "lesson_id": "L02",
      "core_question": "How do you verify that a fix removed the bottleneck?",
      "segment_ids": ["S21", "S22"]
    }
  ],
  "teaching_constraints": {
    "max_interactions": 4,
    "require_visual_text_pair": true
  },
  "course_profile": {
    "audience_level": "beginner",
    "lesson_duration_minutes": 10
  },
  "delivery_constraints": {
    "interaction_density": "medium"
  }
}
```

## Output Snapshot (example)

```json
{
  "lesson_id": "L02",
  "lesson_title": "Verify the Fix",
  "used_variables": ["verification_signal"],
  "depends_on_lessons": ["L01"]
}
```

```md
## Objective
Choose the fastest signal that proves the fix works.
---
?[%{{verification_signal}} p95 latency trend | error-rate slope | lock-wait drop]
---
You selected {{verification_signal}}. Use this as the first verification checkpoint.
```

## Acceptance Notes

- At least one interaction drives downstream text changes.
- Core idea includes visual-plus-text explanation in final script.
- No unresolved placeholders remain in learner-facing text.
