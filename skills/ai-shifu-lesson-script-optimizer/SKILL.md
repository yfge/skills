---
name: ai-shifu-lesson-script-optimizer
description: Audits and improves existing MarkdownFlow teaching prompts to fix coverage gaps, interaction quality, and variable or syntax stability issues.
---

# Lesson Script Optimizer

Systematically improve existing MarkdownFlow teaching prompts. This skill is not for writing a full course from scratch.

## Execution Modes

- Standard mode (default): Source material and current scripts are both available; run full coverage audit and targeted edits.
- Fallback mode: Source material is missing or incomplete; prioritize syntax stability, variable safety, and high-risk interaction fixes.

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
- Optimized learner-facing script output must follow resolved target language unless `bilingual_output` is true.

## When to Use

- You need gap analysis against source material.
- You need script quality upgrades without full rewrites.
- You need consistent chapter style with lower runtime failure risk.

## Minimum Inputs

- Source material (transcript, notes, or structured lesson assets).
- Existing teaching script(s), one lesson or full course.
- Optional constraints (for example, whether cross-lesson variable carryover is allowed).

## Core Method

1. Start with a low-friction entry point (cover visual + one light interaction).
2. Ensure interactions change downstream logic.
3. Keep structure content-driven, not template-driven.
4. Build evidence chain: observation/history -> mechanism/data -> conclusion.
5. Use visuals for abstract structure and text for mechanism + boundaries.
6. Add viewpoint calibration with branching feedback.
7. Include concrete correction actions for major misconceptions.
8. Keep deliverables executable and reusable.
9. Stabilize syntax and variable usage.

## High-Standard Constraints

- Separate knowledge blocks with `---`.
- Include a lesson cover visual by default.
- Keep max interactions per lesson at five (recommended three to four).
- Place interactions at decision points, not only at lesson start.
- Every interaction must trigger immediate feedback plus downstream effect.
- Limit consecutive variable collection to three.
- No uncollected variables in learner-facing text.
- Spread global variable collection across lessons.
- Do not recollect the same variable unless marked as staged comparison.
- Treat semantic duplicates as duplicates even if variable names differ.
- Use stable input syntax: `?[%{{var}}...prompt]`.
- Keep ending structure lesson-appropriate; interactive endings are optional.
- Every core concept needs visual-plus-text explanation.
- Avoid internal authoring terms in learner-facing copy.
- Keep prompts concrete and answerable.
- `*_viewpoint_check` interactions must branch by option.
- Preserve source information density; do not trade substance for fluency.

## MarkdownFlow Syntax (Required)

1. Variables:
- Use `{{var_name}}`.
- Variable names cannot contain spaces.
- Undefined variables default to `"UNKNOWN"`.

2. Interactions:
- Single-select: `?[%{{var}} Option A | Option B | Option C]`
- Multi-select: `?[%{{var}} Option A || Option B || Option C]`
- Input: `?[%{{var}} ... enter your answer]`
- Button + input: `?[%{{var}} Option A | Option B | ...Other, please specify]`

3. Segments:
- Use `---` between modules.
- Keep one objective per module.

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
- Regular text should guide generation behavior.
- Avoid outputting full polished article content as fixed prose.

See `references/methodology.md`.

## Optimization Workflow

1. Define scope (single lesson vs full course).
2. Build coverage matrix: source points -> script coverage.
3. Label issue classes:
- `coverage_gap`
- `meaning_shift`
- `explanation_clarity`
- `interaction_no_branching`
- `visual_constraints_missing`
- `variable_or_syntax_risk`
4. Apply smallest safe edits first.
5. Run checklist validation before final output.
6. Re-check visual-text pairing for every core concept.
7. Re-check variable lifecycle (collection, reference timing, reuse).
8. Re-check semantic duplication in interaction prompts.
9. Re-check viewpoint branching and downstream action coupling.

See `references/review-checklist.md`.

## Required Output Style

- Present conclusion and risk level first.
- Then provide grouped change list by issue class.
- Use file-level references for traceability.
- If duplicate script versions exist, declare the authoritative one.
- If cross-lesson dependency is disallowed, remove dependency text and unbound carryover variables.

## Common Failure Patterns

- Structural edits without content-depth recovery.
- Over-abstraction that drifts from source meaning.
- Hidden cross-lesson variables causing runtime failures.
- Vague prompts that models cannot execute reliably.
- Viewpoint options that still return identical feedback.
- Repeated semantic questions with different variable names.
- Visual tasks without explanatory text.
- Rigid template consistency at the cost of lesson specificity.

## Validation Checkpoints

- Conclusion and risk level are presented first.
- Five issue classes are fully audited.
- `viewpoint_check` interactions branch and trigger distinct next actions.
- Uncollected variable references and semantic duplicate interactions are removed.
- Output remains runnable with no loss of source information density.

## Report Template

See `references/report-template.md`.

## Related Skills

- Upstream preprocessing: `ai-shifu-content-segmenter`
- Upstream orchestration: `ai-shifu-transcript-to-lessons`
- Upstream generation: `ai-shifu-lesson-script-generator`
- Quality governance: `ai-shifu-skill-quality-optimizer`

## Examples

- `examples/minimal.md`
- `examples/edge-case.md`
