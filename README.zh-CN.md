# AI 师傅 Skills（中文说明）

[English README](./README.md)

本仓库聚焦 MarkdownFlow 课程制作，包含 4 个核心 skills。

## 包含的 Skills

- `ai-shifu-content-segmenter`：将杂乱课程素材清洗为稳定的语义课节片段。
- `ai-shifu-transcript-to-lessons`：将逐字稿或文档转换为逐课节 MarkdownFlow 脚本。
- `ai-shifu-lesson-script-generator`：从结构化课节输入生成可运行授课提示词。
- `ai-shifu-lesson-script-optimizer`：审计并优化已有授课提示词的可执行性与稳定性。

每个 skill 都有可运行示例，位于 `skills/<slug>/examples/`。

## 仓库结构

```text
skills/
  ai-shifu-content-segmenter/
  ai-shifu-transcript-to-lessons/
  ai-shifu-lesson-script-generator/
  ai-shifu-lesson-script-optimizer/
```

## 使用说明

每个 skill 以 `SKILL.md` 作为行为定义。
机器可读元数据位于 `skills/<skill-slug>/skill.yaml`。

## 课程生产路径

按控制粒度选择其一：

### 路径 A：一键生成（推荐）

适合希望从原始素材快速得到可运行课程脚本的场景。

1. 准备素材（逐字稿或课程文档）。
2. 运行 `ai-shifu-transcript-to-lessons`。
3. 运行 `ai-shifu-lesson-script-optimizer` 做最终质量加固。

预期产物：
- 分课节 MarkdownFlow 脚本
- 课程索引与全局变量表
- 优化后脚本与风险报告

注意：
- `ai-shifu-transcript-to-lessons` 已内置分段与脚本生成编排。
- 除非你要定向重生成某些课节，否则不要重复运行 `ai-shifu-lesson-script-generator`。

### 路径 B：模块化生产（高级）

适合需要分阶段精细控制的场景。

1. 运行 `ai-shifu-content-segmenter` 生成语义分段与不可变块索引。
2. 运行 `ai-shifu-lesson-script-generator`，按课节定向生成脚本。
3. 运行 `ai-shifu-lesson-script-optimizer`，加固交互逻辑和运行稳定性。

预期产物：
- 结构化分段 JSON
- 可运行 MarkdownFlow 课节脚本
- 带问题级变更追踪的优化脚本

## 元数据校验

```bash
python3 scripts/validate_openai_yaml.py
python3 scripts/validate_skill_quality.py
```

## 语言策略（面向使用者）

这些 skills 支持多语言课程生成，语言决策规则如下：

- 你明确指定输出语言时，优先使用该语言。
- 你提供 `target_language` 时，在没有更强显式指令的情况下按其输出。
- 若未提供上述信息，系统会参考会话偏好和提问语言信号。
- 若仍无法判定，回退到 `en-US`。
- 需要双语输出时，设置 `bilingual_output: true`。

建议使用以下控制项提升可预期性：
- `target_language`（例如 `zh-CN`、`fr-FR`、`ja-JP`）
- `bilingual_output`（`true|false`）
- `term_policy`（`preserve|translate|mixed`）
- `quote_policy`（`translate_only|original_plus_translation`）

## AI 师傅

本技能套件是 AI 师傅课程创作工作流的一部分：https://ai-shifu.com
