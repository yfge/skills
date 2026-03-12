---
name: ai-shifu-transcript-to-lessons
description: Converts long-form transcripts or course documents into lesson-by-lesson MarkdownFlow teaching scripts with stable structure, preserved artifacts, and reusable variables.
---

# Transcript to Lesson Scripts

Convert raw course material into runnable lesson-level MarkdownFlow scripts.

## Execution Modes

- Standard mode (default): Input quality is sufficient; run full pipeline from segmentation to per-lesson script generation and index assembly.
- Fallback mode: Input is incomplete or low quality; produce coarse lesson drafts, mark uncertainty, and provide focused rerun hints.

## Language Resolution Policy

Resolve target language with this strict priority:

1. `explicit_output_language_request`
2. `target_language_parameter`
3. `session_language_preference`
4. `prompt_language_detection`
5. `source_material_dominant_language`
6. `default_fallback_language`

Use these optional control fields:

- `target_language` (BCP-47 recommended, for example `fr-FR`, `ja-JP`, `zh-CN`)
- `bilingual_output` (`true|false`)
- `term_policy` (`preserve|translate|mixed`)
- `quote_policy` (`translate_only|original_plus_translation`)

Policy constraints:

- Do not limit supported languages to a predefined set.
- If explicit language output is requested, do not let mixed-source language override it.

## Output Boundary

- Final outputs start with learner-facing teaching content.
- Authoring rules and pipeline notes stay in skill docs and references, not in lesson outputs.

## Workflow

1. Normalize source ordering and merge input material.
2. Call `ai-shifu-content-segmenter` for cleanup and semantic segmentation.
3. Generate lesson-cut candidates with one core question each.
4. Call `ai-shifu-lesson-script-generator` for lesson-level MarkdownFlow scripts.
5. Build course index and global variable table.
6. Recompute only failed lessons through strict gating.

## Input Contract

At least one of the following is required:

- A single long transcript or course document.
- Multiple topic-aligned documents with ordering metadata.

Optional constraints:

- Learner persona.
- Lesson granularity (`short`, `medium`, `long`).
- Terminology and tone preservation requirements.
- `course_profile` (json): audience level, prerequisite level, lesson duration target, lesson count target, and assessment mode.
- `delivery_constraints` (json): interaction density, platform limits, must-cover topics, avoid topics, and non-negotiable source fragments.

See `references/input-contract.md`.

## Output Contract

Return:

- Lesson MarkdownFlow scripts (one file per lesson).
- Course index (lesson id, title, core question, source mapping).
- Global variable table (definition, use, cross-lesson references).

See `references/output-contract.md`.

## Mandatory Gates

All gates must pass:

- Code blocks are preserved character-by-character.
- Image links and relative placement are preserved.
- Each lesson resolves one core question.
- Each lesson contains at least one valid MarkdownFlow interaction, max five interactions total.
- Each lesson includes a minimum teaching loop: setup, explanation, interaction, close.
- Lesson language is learner-facing, not pipeline narration.
- Each lesson includes at least one deepening interaction (calibration, boundary check, or counterintuitive prompt).
- Action tasks are either immediately executable or explicitly linked to later modules.
- Variable naming is consistent and traceable.
- No unresolved placeholder variables in learner-facing text.
- Do not wrap full lessons in deterministic blocks (`=== ===` or `!=== !===`).
- Deterministic blocks are reserved for legally or operationally fixed statements only.
- If an image must remain unchanged, use single-line deterministic syntax per image.
- Use `---` between instructional blocks to keep pacing readable.
- Every variable collection step must produce immediate feedback and downstream effect.
- Core knowledge points require visual + textual explanation together.
- Consecutive variable collection cannot exceed three variables.
- Do not recollect the same variable unless explicitly marked as staged comparison.
- Never reference uncollected variables.
- Interaction prompts must be concrete and directly answerable.
- Avoid repetitive interaction semantics across lessons unless comparison intent is explicit.
- `*_viewpoint_check` interactions must branch by option and drive different next steps.
- Every interaction variable must create visible downstream impact.

See `references/preservation-rules.md` and `references/markdownflow-spec.md`.

## MarkdownFlow Syntax (Required)

1. Variables:

- Use `{{var_name}}` for variable references.
- Variable names cannot contain spaces.
- Undefined variables default to `"UNKNOWN"`.

2. Interactions:

- Single-select: `?[%{{var}} Option A | Option B | Option C]`
- Multi-select: `?[%{{var}} Option A || Option B || Option C]`
- Input: `?[%{{var}} ... enter your answer]`
- Button + input: `?[%{{var}} Option A | Option B | ...Other, please specify]`

3. Segments:

- Use `---` between segments.
- Each segment should serve one clear instructional objective.

4. Deterministic output:

- Single-line fixed text: `===fixed text===`
- Multi-line fixed text:

```md
!===
Line 1
Line 2
!===
```

5. Authoring rule:

- Regular content should guide generation behavior.
- Do not output full polished learner prose as static text.

## Rerun Rules

- Recompute only impacted lessons.
- Recompute dependency-linked lessons when shared variables change.
- Recompute full course only when global source order changes.

## Failure Handling

When source quality is weak:

- Deliver coarse lesson drafts first.
- Mark uncertain spans explicitly.
- Continue with best-effort generation instead of stopping.

## Validation Checkpoints

- Lesson scripts, course index, and variable table are all present.
- Code/image preservation is exact and position-safe.
- One-core-question and interaction cap rules are satisfied per lesson.
- No unresolved variables or no-op interactions remain.
- Fallback outputs include explicit uncertainty markers and rerun hints.

## Report Template

See `references/report-template.md`.

## Related Skills

- Upstream cleanup: `ai-shifu-content-segmenter`
- Downstream generation: `ai-shifu-lesson-script-generator`
- Downstream optimization: `ai-shifu-lesson-script-optimizer`

## Examples

- `examples/minimal.md`
- `examples/edge-case.md`
