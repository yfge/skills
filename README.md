# ai-shifu skills

[Alternate README Path](./README.zh-CN.md)

A consolidated repository of five AI-Shifu skills for MarkdownFlow course production and skill quality governance.

## Included Skills

- `ai-shifu-content-segmenter`: clean noisy source material into stable semantic lesson segments.
- `ai-shifu-transcript-to-lessons`: convert transcripts or documents into lesson-by-lesson MarkdownFlow scripts.
- `ai-shifu-lesson-script-generator`: generate runnable lesson prompts from structured lesson inputs.
- `ai-shifu-lesson-script-optimizer`: audit and improve existing MarkdownFlow teaching prompts.
- `ai-shifu-skill-quality-optimizer`: audit and improve repository quality using blocker/suggestion gating.

Each skill includes runnable examples under `skills/<slug>/examples/`.

## Repository Layout

```text
skills/
  ai-shifu-content-segmenter/
  ai-shifu-transcript-to-lessons/
  ai-shifu-lesson-script-generator/
  ai-shifu-lesson-script-optimizer/
  ai-shifu-skill-quality-optimizer/
```

## Usage

Each skill keeps `SKILL.md` as the behavior source of truth.
Operational metadata lives in `skills/<skill-slug>/skill.yaml`.

## Unified Quickstart

Goal: run the four core lesson skills as one pipeline from noisy source material to optimized teaching prompts.

1. Prepare source material (transcript or course document).
2. Run `ai-shifu-content-segmenter` to produce stable segment candidates and immutable-block indexes.
3. Run `ai-shifu-transcript-to-lessons` to generate lesson-by-lesson MarkdownFlow scripts.
4. Run `ai-shifu-lesson-script-generator` to produce runnable lesson prompts.
5. Run `ai-shifu-lesson-script-optimizer` to improve teaching logic, interaction quality, and variable stability.

Expected artifacts:

- Structured segmentation JSON
- Lesson-by-lesson MarkdownFlow scripts
- Optimized lesson prompts and audit notes

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
