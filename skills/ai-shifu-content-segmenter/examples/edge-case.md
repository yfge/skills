# Edge Case Example

## Input Payload (example)

```json
{
  "raw_material": "doc-a: retries should stop after 3 attempts...\ndoc-b: retries can continue until queue drains...\ndoc-c: [image:failure-matrix.png]",
  "course_profile": {
    "audience_level": "intermediate",
    "lesson_duration_minutes": 15
  },
  "delivery_constraints": {
    "must_cover_topics": ["stop condition design"],
    "non_negotiable_fragments": ["[image:failure-matrix.png]"]
  }
}
```

## Output Snapshot (example)

```json
{
  "structured_segments_json": [
    {
      "segment_id": "S10",
      "segment_type": "concept",
      "core_point": "Retry stop conditions differ across sources.",
      "source_span": {"start": 0, "end": 95},
      "uncertainty": "high"
    },
    {
      "segment_id": "S11",
      "segment_type": "image",
      "core_point": "Failure matrix image preserved",
      "preserve_block": "yes",
      "source_span": {"start": 96, "end": 132}
    }
  ],
  "preserve_block_index": [
    {"block_id": "B07", "type": "image", "segment_id": "S11"}
  ],
  "lesson_cut_candidates": [
    {
      "lesson_id": "L04",
      "segment_ids": ["S10", "S11"],
      "core_question": "How should stop conditions change by failure type?",
      "needs_rerun": true
    }
  ],
  "rerun_hints": [
    "Provide authoritative policy for max retry attempts.",
    "Confirm whether queue-drain mode is allowed in this course."
  ]
}
```

## Acceptance Notes

- Fallback mode is explicit.
- Conflicts are surfaced as uncertainty, not silently merged.
- Output schema remains compatible for downstream skills.
