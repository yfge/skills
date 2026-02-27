---
name: mdf-material-adapter
description: 对杂乱逐字稿或课程文档进行清洗、结构化和语义分段，输出稳定的课节切分候选，同时保留代码、图片和关键术语。Use when raw course materials are noisy before MarkdownFlow lesson generation.
---

# 课程资料适配器

把噪声较高的课程资料整理成可稳定生成课节的中间结构。

## 执行流程

1. 去除口头赘词与重复片段，不改变原意。
2. 标记不可改写块：代码、图片、表格。
3. 按语义连续性分段，不仅依赖标题层级。
4. 生成课节边界候选，保证单节单核心问题。
5. 返回带源片段映射的结构化分段。

## 分段结构

每个分段返回：
- `segment_id`
- `segment_type`（`concept`、`example`、`code`、`image`、`exercise`、`transition`）
- `core_point`
- `preserve_block`（`yes` 或 `no`）
- `source_span`

## 保真规则

必须保留：
- 代码内容与 fence 类型。
- 图片 URL、alt 文本、相对位置。
- 专有术语与关键事实口径。

允许改写：
- 口头填充词。
- 断句与标点修复。
- 冗余过渡语。

## 迁移友好规则

为后续教学迁移保留以下信息：
- `learner-hook`：可直接触发用户思考的原句或问题。
- `evidence-type`：历史/现象/数据/机制/结论标签。
- `visual-cue`：适合做 HTML 或 SVG 可视化的片段标记。
- `concept-conflict`：可形成认知冲突的观点对。
- `boundary-cue`：结论成立/失效边界线索。
- `action-cue`：可形成“当下可启动”或“后续模块联动”的行动线索。
- `density-cue`：高信息密度句群标记（避免后续生成时被过度稀释）。
- `quote-cue`：可保留原句语气的关键表达（用于提升讲解原味与准确度）。
- `visual-text-pair-cue`：建议“先图后文”的知识点配对线索。
- `interaction-intent-cue`：互动问题意图标签（分层/分流/校准/对照），用于避免同义重复提问。
- `compare-cue`：适合做“前后对照/阶段演进”复采的问题线索。

## 输出

输出结果：
- 有序分段列表。
- 课节切分候选。
- 每节核心问题。
- 保真块索引。
- 迁移线索（`learner-hook`、`evidence-type`、`visual-cue`、`concept-conflict`、`boundary-cue`、`action-cue`、`density-cue`、`quote-cue`、`visual-text-pair-cue`、`interaction-intent-cue`、`compare-cue`）。

详见 `references/segmentation-rules.md`。
