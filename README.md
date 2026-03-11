# AI-Shifu Skills

[Alternate README Path](./README.zh-CN.md)

A consolidated repository of four core AI-Shifu skills for MarkdownFlow course production.

## Included Skills

- `ai-shifu-content-segmenter`: clean noisy source material into stable semantic lesson segments.
- `ai-shifu-transcript-to-lessons`: convert transcripts or documents into lesson-by-lesson MarkdownFlow scripts.
- `ai-shifu-lesson-script-generator`: generate runnable lesson prompts from structured lesson inputs.
- `ai-shifu-lesson-script-optimizer`: audit and improve existing MarkdownFlow teaching prompts.

Each core skill includes runnable examples under `skills/<slug>/examples/`.

The quality-governance skill is intentionally decoupled and kept as a standalone module under:

- `standalone-skills/ai-shifu-skill-quality-optimizer`

## Repository Layout

```text
skills/
  ai-shifu-content-segmenter/
  ai-shifu-transcript-to-lessons/
  ai-shifu-lesson-script-generator/
  ai-shifu-lesson-script-optimizer/
standalone-skills/
  ai-shifu-skill-quality-optimizer/
```

## Usage

Each skill keeps `SKILL.md` as the behavior source of truth.
Core skill metadata lives in `skills/<skill-slug>/skill.yaml`.
The standalone quality optimizer metadata lives in `standalone-skills/ai-shifu-skill-quality-optimizer/skill.yaml`.

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

## Build Catalog Artifacts

Generate machine-readable catalog files for indexing, search, and distribution:

```bash
python3 scripts/build_catalog.py
```

Output files:

- `catalog/skills.json`
- `catalog/skills.csv`
- `INDEX.md`

## Validate Metadata

```bash
python3 scripts/validate_openai_yaml.py
python3 scripts/validate_skill_quality.py
python3 scripts/build_catalog.py
python3 scripts/build_quality_report.py
```

Quality artifacts:

- `quality/quality-report.md`
- `quality/quality-summary.json`

## Stability Task Boards

Atomic quality and stability iterations are tracked in:

- `tasks/skill-stability-v1/backlog.yaml`
- `tasks/skill-stability-v1/iteration-log.md`
- `tasks/skill-stability-v2/backlog.yaml`
- `tasks/skill-stability-v2/iteration-log.md`

## Language Policy

All skill artifacts are authored in international English to support global distribution.

## AI-Shifu

This suite is part of AI-Shifu's course authoring workflow: https://ai-shifu.com
