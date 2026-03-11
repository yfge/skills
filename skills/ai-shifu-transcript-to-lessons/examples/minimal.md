# Minimal Example

## Input Payload (example)

```json
{
  "course_material": "Module transcript: observe metric drift, classify causes, apply one fix, review impact.",
  "generation_constraints": {
    "persona": "practical coach",
    "lesson_granularity": "short"
  },
  "course_profile": {
    "audience_level": "beginner",
    "lesson_duration_minutes": 10,
    "lesson_count_target": 3,
    "assessment_mode": "project"
  },
  "delivery_constraints": {
    "interaction_density": "medium",
    "must_cover_topics": ["diagnosis", "verification"]
  },
  "target_language": "en-US"
}
```

## Output Snapshot (example)

```json
{
  "course_index": [
    {
      "lesson_id": "L01",
      "lesson_title": "Observe and Classify",
      "core_question": "Which signal separates symptom from root cause?",
      "source_span_map": [{"source_id": "course_material", "start": 0, "end": 64}]
    }
  ],
  "global_variable_table": [
    {
      "name": "diagnosis_choice",
      "collected_in": "L01",
      "used_in": ["L01", "L02"],
      "effect_scope": "cross_lesson"
    }
  ]
}
```

```md
## L01 Objective
Identify the highest-signal diagnostic step.
---
?[%{{diagnosis_choice}} check workload shape | check lock wait | check cache hit ratio]
---
Based on {{diagnosis_choice}}, we run one focused verification next.
```

## Acceptance Notes

- One core question is defined per lesson.
- Variables are collected before use and reused consistently.
- Output is learner-facing and runnable.
