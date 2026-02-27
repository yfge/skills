# MarkdownFlow 规范（官方口径）

来源：
- https://markdownflow.ai/docs/zh/
- https://markdownflow.ai/docs/zh/overview/
- https://markdownflow.ai/docs/zh/reference/syntax/
- https://markdownflow.ai/docs/zh/reference/variables/

## 关键规则

1. `=== ... ===` 仅用于固定内容块（保持不变）。
2. 不要把整段授课内容都包进 `=== ... ===`，否则模型无法演绎。
3. 授课提示词文件必须从正式授课内容开始，不包含方法说明。
4. 交互语句与变量赋值要可执行，交互后必须有响应。
5. 变量采集要分散，减少单轮用户负担。

## 项目约束（本技能额外要求）

1. 每个模块尽量只采集 1 个变量。
2. 每个变量必须改变后续讲解或交付物。
3. 章节结尾统一使用“总结”命名。
