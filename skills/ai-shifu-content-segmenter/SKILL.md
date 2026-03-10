---
name: ai-shifu-content-segmenter
description: Cleans noisy transcripts and course documents, then produces stable semantic lesson segments while preserving code, images, and critical terminology.
---

# Course Material Segmenter

Turn messy course source material into a reliable intermediate structure for downstream lesson generation.

## Execution Modes

- Standard mode (default): Input is complete enough to run full cleanup, semantic segmentation, and lesson-boundary extraction.
- Fallback mode: Input is incomplete or out of order; produce coarse segments first, flag uncertainty, and preserve traceability for targeted reruns.

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

Notes:
- Do not restrict supported languages to a fixed list.
- If output language is explicit, source-language distribution must not override it.

## Workflow

1. Remove filler language and duplicated phrasing without changing meaning.
2. Mark immutable blocks: code, images, and tables.
3. Segment by semantic continuity instead of headings alone.
4. Propose lesson boundaries with one core question per lesson.
5. Return source-linked structured segments.

## Segment Schema

Each segment includes:
- `segment_id`
- `segment_type` (`concept`, `example`, `code`, `image`, `exercise`, `transition`)
- `core_point`
- `preserve_block` (`yes` or `no`)
- `source_span`

## Preservation Rules

Must preserve:
- Code content and fence language.
- Image URLs, alt text, and relative placement.
- Domain terms and factual statements.

Can normalize:
- Speech filler.
- Sentence breaks and punctuation.
- Redundant transitions.

## Transfer Signals

Capture these fields for downstream teaching quality:
- `learner_hook`: statements that can trigger learner reflection.
- `evidence_type`: one of history, phenomenon, data, mechanism, or conclusion.
- `visual_cue`: fragments suited for SVG/HTML visual support.
- `concept_conflict`: candidate idea conflicts for cognitive contrast.
- `boundary_cue`: clues for validity boundaries.
- `action_cue`: clues that can become immediate or staged actions.
- `density_cue`: high-information chunks that should not be diluted.
- `quote_cue`: original wording worth preserving.
- `visual_text_pair_cue`: clues for "visual first, explanation second" blocks.
- `interaction_intent_cue`: intent labels such as diagnose, branch, calibrate, compare.
- `compare_cue`: candidate prompts for before/after comparison.

## Outputs

- Ordered segment list.
- Lesson boundary candidates.
- One core question per lesson.
- Preservation block index.
- Full transfer-signal package.

See `references/segmentation-rules.md`.

## Validation Checkpoints

- Segment output covers all valid source spans in traceable order.
- Code/image/table blocks keep original placement and format.
- Every lesson candidate resolves to one core question.
- Transfer-signal fields are complete and usable downstream.
- Cleanup does not alter key facts or terminology.

## Report Template

See `references/report-template.md`.

## Related Skills

- Downstream orchestration: `ai-shifu-transcript-to-lessons`
- Downstream script generation: `ai-shifu-lesson-script-generator`
- Quality governance: `ai-shifu-skill-quality-optimizer`

## Examples

- `examples/minimal.md`
- `examples/edge-case.md`
