# AI-Shifu Skills

[中文 README](./README.zh-CN.md)

A consolidated repository of five core AI-Shifu skills for MarkdownFlow course production and deployment.

## Included Skills

- `ai-shifu-content-segmenter`: clean noisy source material into stable semantic lesson segments.
- `ai-shifu-transcript-to-lessons`: convert transcripts or documents into lesson-by-lesson MarkdownFlow scripts.
- `ai-shifu-lesson-script-generator`: generate runnable lesson prompts from structured lesson inputs.
- `ai-shifu-lesson-script-optimizer`: audit and improve existing MarkdownFlow teaching prompts.
- `ai-shifu-course-manager`: deploy, manage, and sync MDF course files to the AI-Shifu platform.

The four authoring skills include runnable examples under `skills/<slug>/examples/`.

## Repository Layout

```text
skills/
  ai-shifu-content-segmenter/
  ai-shifu-transcript-to-lessons/
  ai-shifu-lesson-script-generator/
  ai-shifu-lesson-script-optimizer/
  ai-shifu-course-manager/
```

## Usage

Each skill keeps `SKILL.md` as the behavior source of truth.
Core skill metadata lives in `skills/<skill-slug>/skill.yaml`.

## Course Authoring Paths

Choose one path based on control needs:

### Path A: One-Shot Generation (Recommended)

Use when you want the fastest route from raw material to runnable lesson scripts.

1. Prepare source material (transcript or course documents).
2. Run `ai-shifu-transcript-to-lessons`.
3. Run `ai-shifu-lesson-script-optimizer` for final quality hardening.

Expected artifacts:
- Lesson-by-lesson MarkdownFlow scripts
- Course index and global variable table
- Optimized lesson prompts and risk report

Note:
- `ai-shifu-transcript-to-lessons` already orchestrates segmentation and lesson script generation internally.
- Do not run `ai-shifu-lesson-script-generator` again unless you are intentionally regenerating selected lessons.

### Path B: Modular Authoring (Advanced)

Use when you need precise control over each stage.

1. Run `ai-shifu-content-segmenter` to produce semantic segments and immutable-block indexes.
2. Run `ai-shifu-lesson-script-generator` lesson by lesson on selected segments.
3. Run `ai-shifu-lesson-script-optimizer` to harden interaction logic and runtime stability.

Expected artifacts:
- Structured segmentation JSON
- Runnable lesson MarkdownFlow scripts
- Optimized scripts with issue-level change traceability

## Validate Metadata

```bash
python3 scripts/validate_skill_quality.py
```

## Language Policy

Skills are language-flexible for course generation. From a user perspective:

- If you explicitly request an output language, that language is used.
- If you provide `target_language`, it is used when no stronger explicit instruction exists.
- If neither is provided, the system uses session preference and prompt language signals.
- If language is still ambiguous, it falls back to `en-US`.
- If you need bilingual output, set `bilingual_output: true`.

Recommended controls for predictable language output:
- `target_language` (for example `zh-CN`, `fr-FR`, `ja-JP`)
- `bilingual_output` (`true|false`)
- `term_policy` (`preserve|translate|mixed`)
- `quote_policy` (`translate_only|original_plus_translation`)

## Course Deployment

Once your MarkdownFlow scripts are ready, use `ai-shifu-course-manager` to deploy them to the AI-Shifu platform:

1. Build the import file from a local course directory: `build --course-dir ./course-a/`
2. Import to the platform: `import --new --json-file ./course-a/shifu-import.json`
3. Publish the course: `publish <shifu_bid>`

See the [Course Manager SKILL.md](./skills/ai-shifu-course-manager/SKILL.md) for full CLI reference.

## AI-Shifu

This suite is part of AI-Shifu's course authoring workflow: https://ai-shifu.com
