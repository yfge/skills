# Input Contract

## Required

Provide one of:
- A single long transcript or course document.
- A set of topic-aligned documents with intended order.

## Optional

- Learner persona.
- Lesson granularity preference (`short`, `medium`, `long`).
- Terminology and tone constraints.
- Non-negotiable source fragments.
- `target_language` (BCP-47 recommended, for example `fr-FR`, `ja-JP`, `zh-CN`).
- `bilingual_output` (`true|false`).
- `term_policy` (`preserve|translate|mixed`).
- `quote_policy` (`translate_only|original_plus_translation`).

## Language Resolution Priority

If language signals conflict, resolve with this strict order:
1. explicit output language request
2. `target_language` parameter
3. session language preference
4. prompt language detection
5. source-material dominant language
6. default fallback language (`en-US`)

## Validation Rules

- Input files must be readable text or markdown.
- If multiple files are provided, ordering must be explicit.
- Source language and expected output language should be specified when multilingual content exists.
- Explicit output language requests must not be overridden by source-language mixes.
