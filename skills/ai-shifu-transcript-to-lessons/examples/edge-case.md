# Edge Case Example

## Input Payload (example)

```json
{
  "course_material": "doc-1: classify by latency tiers\n\ndoc-2: classify by resource contention\n\ndoc-3: missing section ordering",
  "generation_constraints": {
    "lesson_granularity": "medium"
  },
  "course_profile": {
    "audience_level": "intermediate",
    "lesson_duration_minutes": 15
  },
  "delivery_constraints": {
    "must_cover_topics": ["classification tradeoffs"],
    "platform_limits": ["markdown_only"]
  }
}
```

## Output Snapshot (example)

```json
{
  "course_index": [
    {
      "lesson_id": "L03",
      "lesson_title": "Choose a Classification Axis",
      "core_question": "When should you prefer latency tiers over contention classes?",
      "source_span_map": [{"source_id": "doc-1", "start": 0, "end": 33}],
      "uncertainty": "medium"
    }
  ],
  "global_variable_table": [
    {
      "name": "classification_axis",
      "collected_in": "L03",
      "used_in": ["L03"],
      "effect_scope": "local"
    }
  ],
  "rerun_plan": {
    "lessons_to_rerun": ["L03"],
    "reason": "conflicting taxonomy across doc-1 and doc-2"
  }
}
```

```md
## L03 Objective
Select a first-pass classification rule.
---
?[%{{classification_axis}} latency first | contention first]
---
Current evidence is partial; confirm one canonical taxonomy before final pass.
```

## Acceptance Notes

- Pipeline returns partial but runnable output instead of failing hard.
- Uncertainty and rerun scope are explicit.
- Downstream optimizer can continue incrementally.
