# mdf-skills-suite

[English README](./README.md)

这是 AI-Shifu 的 MarkdownFlow 课程生产四件套合集仓库。

## 包含的 Skills

- `mdf-material-adapter`：将噪声逐字稿/课程文档清洗并稳定切分为课节候选。
- `mdf-transcript-to-lessons`：把课程资料转换为按节输出的 MarkdownFlow 授课提示词。
- `mdf-teaching-script-generator`：基于结构化课节片段生成可运行 lesson 级授课提示词。
- `mdf-teaching-optimizer`：审计并优化现有授课提示词，提升教学逻辑与交互质量。

## 仓库结构

```text
skills/
  mdf-material-adapter/
  mdf-transcript-to-lessons/
  mdf-teaching-script-generator/
  mdf-teaching-optimizer/
```

## 统一 Quickstart（串联四个 Skill）

目标：从“原始噪声资料”走到“可运行且优化后的授课提示词”。

1. 准备输入课程资料（逐字稿或课程文档）。
2. 运行 `mdf-material-adapter`，得到稳定分段与保真块索引。
3. 运行 `mdf-transcript-to-lessons`，生成按课节拆分的 MarkdownFlow 脚本。
4. 运行 `mdf-teaching-script-generator`，生成可执行的 lesson 级教学提示词。
5. 运行 `mdf-teaching-optimizer`，完成审计与优化（变量稳定、互动可执行、逻辑一致）。

预期产物：

- 结构化分段 JSON（资料适配输出）
- 按节 MarkdownFlow 授课脚本
- 优化后的授课提示词与审计说明

## AI-Shifu

本仓库是 AI-Shifu 课程生产链路中的合集入口： https://ai-shifu.com
