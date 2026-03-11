# AI-Shifu Skills

[English README](./README.md)

一个整合了五个 AI-Shifu 技能的仓库，用于 MarkdownFlow 课程制作与技能质量治理。

## 包含的技能

- `ai-shifu-content-segmenter`：将杂乱的原始素材清洗为稳定的语义课节片段。
- `ai-shifu-transcript-to-lessons`：将逐字稿或文档转换为按课节输出的 MarkdownFlow 脚本。
- `ai-shifu-lesson-script-generator`：从结构化的课节输入生成可运行的课程提示词。
- `ai-shifu-lesson-script-optimizer`：审计并优化现有的 MarkdownFlow 授课提示词。
- `ai-shifu-skill-quality-optimizer`：使用 blocker/suggestion 门控机制审计并提升仓库质量。

每个技能在 `skills/<slug>/examples/` 下都包含可运行的示例。

## 仓库结构

```text
skills/
  ai-shifu-content-segmenter/
  ai-shifu-transcript-to-lessons/
  ai-shifu-lesson-script-generator/
  ai-shifu-lesson-script-optimizer/
  ai-shifu-skill-quality-optimizer/
```

## 使用方式

每个技能以 `SKILL.md` 作为行为定义的唯一真实来源。
运行元数据存放在 `skills/<skill-slug>/skill.yaml` 中。

## 统一快速上手

目标：将四个核心课程技能作为一条流水线运行，从杂乱的原始素材到优化后的授课提示词。

1. 准备原始素材（逐字稿或课程文档）。
2. 运行 `ai-shifu-content-segmenter` 生成稳定的分段候选和不可变块索引。
3. 运行 `ai-shifu-transcript-to-lessons` 生成按课节划分的 MarkdownFlow 脚本。
4. 运行 `ai-shifu-lesson-script-generator` 生成可运行的课程提示词。
5. 运行 `ai-shifu-lesson-script-optimizer` 优化教学逻辑、交互质量和变量稳定性。

预期产出物：

- 结构化分段 JSON
- 按课节划分的 MarkdownFlow 脚本
- 优化后的课程提示词和审计说明

## 构建目录产出物

生成机器可读的目录文件，用于索引、搜索和分发：

```bash
python3 scripts/build_catalog.py
```

输出文件：

- `catalog/skills.json`
- `catalog/skills.csv`
- `INDEX.md`

## 验证元数据

```bash
python3 scripts/validate_openai_yaml.py
python3 scripts/validate_skill_quality.py
python3 scripts/build_catalog.py
python3 scripts/build_quality_report.py
```

质量产出物：

- `quality/quality-report.md`
- `quality/quality-summary.json`

## 稳定性任务看板

原子级的质量和稳定性迭代记录在：

- `tasks/skill-stability-v1/backlog.yaml`
- `tasks/skill-stability-v1/iteration-log.md`
- `tasks/skill-stability-v2/backlog.yaml`
- `tasks/skill-stability-v2/iteration-log.md`

## 语言策略

所有技能产出物均以国际英文编写，以支持全球分发。

## AI-Shifu

本技能套件是 AI-Shifu 课程创作工作流的一部分：https://ai-shifu.com
