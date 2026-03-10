---
name: ai-shifu-lesson-script-generator
description: Generates runnable lesson-level MarkdownFlow teaching prompts from structured lesson segments, with safe interaction logic and stable variable reuse.
---

# Lesson Script Generator

Generate runnable MarkdownFlow scripts for each lesson.

## Execution Modes

- Standard mode (default): Structured lesson input is complete; generate full scripts with interaction branching and variable reuse.
- Fallback mode: Input is minimal; generate stable baseline scripts first, then enrich depth after additional context is supplied.

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

Output rule:
- Learner-facing script text must follow resolved target language unless `bilingual_output` is true.

## Output Boundary

- Output learner-facing teaching prompt content only.
- Do not include process notes, author instructions, or policy notes in final script output.
- Internal design notes may appear only in HTML comments when needed.

## Teaching Pattern Baseline

Use these defaults unless lesson content requires a justified variation:

1. Learner-facing language only.
2. Variable collection is distributed, not front-loaded.
3. Build evidence chain from observation to mechanism to conclusion.
4. Use visual-first explanation for abstract concepts, then textual interpretation.
5. Every collected variable must immediately affect downstream content.
6. Include at least one deepening interaction (calibration, boundary check, or misconception correction).
7. Include at least one reusable deliverable.
8. Action steps must be immediately executable or explicitly staged for downstream lessons.
9. Use carryover statements only if cross-lesson dependency is allowed.
10. Avoid exposing internal authoring terms in learner-facing text.
11. Keep interaction prompts concrete and answerable.
12. `*_viewpoint_check` prompts must branch with distinct feedback paths.
13. Repeated interaction patterns are allowed only when framed as staged comparison.

## Single-Lesson Generation Strategy

Required anchors:
1. Opening objective plus visual cover.
2. Evidence-chain explanation.
3. At least one effective interaction with visible downstream effect.
4. At least one reusable deliverable.
5. Lesson close with summary or decision checkpoint.

Optional modules:
- Viewpoint calibration.
- Misconception correction.
- Dual deliverables (understanding + action).
- Cross-lesson bridge sentence.
- Additional visual-text reinforcement blocks.

## MarkdownFlow Rules

- Use `=== ... ===` only for fixed text that must remain unchanged.
- Never lock full lesson bodies inside deterministic blocks.
- For fixed images, use one deterministic line per image.
- Use `---` to separate instructional modules.
- After each interaction, restate learner selection and reflect it in downstream content.
- For input prompts, include example phrasing to reduce blank responses.
- Use stable input syntax: `?[%{{var}}...prompt]`.

See `references/markdownflow-spec.md`, `references/example-teaching-patterns.md`, and `references/cognitive-teaching-techniques.md`.

## MarkdownFlow Syntax (Required)

1. Variables:
- Use `{{var_name}}` for references.
- Variable names cannot contain spaces.
- Undefined variables default to `"UNKNOWN"`.

2. Interactions:
- Single-select: `?[%{{var}} Option A | Option B | Option C]`
- Multi-select: `?[%{{var}} Option A || Option B || Option C]`
- Input: `?[%{{var}} ... enter your answer]`
- Button + input: `?[%{{var}} Option A | Option B | ...Other, please specify]`

3. Segments:
- Use `---` to split modules.
- Keep one clear objective per module.

4. Deterministic output:
- Single-line fixed text: `===fixed text===`
- Multi-line fixed text:
```md
!===
Line 1
Line 2
!===
```

5. Authoring principle:
- Script text should guide generation behavior.
- Avoid dumping fully polished end-learner prose as fixed output.

## Variable Strategy

- Prefer at most one variable collection per module.
- Max five interactions per lesson (recommended three to four).
- No more than three consecutive variable collections before feedback.
- Reuse global variables when possible; add lesson-local variables only when required.
- Every variable must have downstream utility (branching, depth control, or deliverable variation).
- No unresolved placeholders in learner-facing text.
- Do not recollect the same variable unless explicitly marked as staged comparison.
- Prevent semantic duplicates even when variable names differ.

## Visual-Text Coordination Constraints

- Include an SVG cover in each lesson by default.
- Every core concept must include at least one visual-plus-explanation pair.
- Visuals compress structure; text explains mechanism, limits, and pitfalls.
- Replace unstable source images with generated SVG/HTML visuals when needed.

## Interaction Design Constraints

- Use no more than one `viewpoint_check` in a lesson unless justified.
- Each `viewpoint_check` must trigger a concrete next action.
- If using a "restate-boundary-counterintuitive" pattern, branch by option with distinct content.

## Output Structure

Return per lesson:
- `lesson_id`
- `lesson_title`
- `mdf_script`
- `used_variables`
- `depends_on_lessons`

See `references/lesson-template.md`.

## Validation Checkpoints

- Minimum teaching loop exists (setup, explanation, interaction, close).
- Interaction outcomes visibly alter downstream content.
- Variable safety rules pass (collect before reference, no duplicate recollection).
- Core concepts satisfy visual-plus-text coordination.
- Script remains valid and runnable MarkdownFlow.

## Report Template

See `references/report-template.md`.

## Related Skills

- Upstream preprocessing: `ai-shifu-content-segmenter`
- Upstream orchestration: `ai-shifu-transcript-to-lessons`
- Downstream optimization: `ai-shifu-lesson-script-optimizer`
- Quality governance: `ai-shifu-skill-quality-optimizer`

## Examples

- `examples/minimal.md`
- `examples/edge-case.md`
