# Output Contract

## Required Artifacts

1. `lesson_mdf_scripts`
- One MarkdownFlow file per lesson.
- Learner-facing language only.

2. `course_index`
- `lesson_id`
- `lesson_title`
- `core_question`
- `source_span_map`

3. `global_variable_table`
- Variable name
- Collection point
- Downstream usage
- Cross-lesson dependencies

## Delivery Guarantees

- Stable schema across reruns.
- Deterministic references for lesson ids and source spans.
- Partial rerun support for changed lessons.
