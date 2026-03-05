# ai-shifu-skills

[中文文档](./README.zh-CN.md)

A consolidated repository of 4 MarkdownFlow course-production skills from AI-Shifu.

## Included Skills

- `mdf-material-adapter`: clean noisy raw materials into stable lesson segmentation candidates.
- `mdf-transcript-to-lessons`: convert transcript/document materials into lesson-by-lesson MarkdownFlow scripts.
- `mdf-teaching-script-generator`: generate runnable lesson prompts from structured lesson segments.
- `mdf-teaching-optimizer`: audit and optimize existing MarkdownFlow teaching prompts.

## Repository Layout

```text
skills/
  mdf-material-adapter/
  mdf-transcript-to-lessons/
  mdf-teaching-script-generator/
  mdf-teaching-optimizer/
```

## Usage

Each skill keeps its own `SKILL.md` as the source of truth.

## Unified Quickstart

Goal: run the 4 skills as one pipeline from noisy source material to optimized lesson prompts.

1. Prepare source material (transcript or course document).
2. Run `mdf-material-adapter` to produce stable segment candidates and preserved block index.
3. Run `mdf-transcript-to-lessons` to convert structured material into lesson-level MarkdownFlow scripts.
4. Run `mdf-teaching-script-generator` to generate runnable per-lesson teaching prompts.
5. Run `mdf-teaching-optimizer` to audit and optimize teaching logic, interaction quality, and variable stability.

Expected artifacts:

- Structured segmentation JSON (adapter output)
- Lesson-by-lesson MarkdownFlow scripts
- Optimized teaching prompt set and review notes

## AI-Shifu

This suite is part of AI-Shifu's course authoring workflow: https://ai-shifu.com
