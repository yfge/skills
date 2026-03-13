---
name: ai-shifu-course-deployer
description: 将本地 MDF 课程文件同步到 AI-Shifu 平台。支持生成导入 JSON、通过 API 或 CLI 导入课程。适用于：MDF 课程部署、课程更新同步、批量导入。
user-invocable: true
metadata: {"openclaw": {"emoji": "🚀"}}
---

# MDF → AI-Shifu 同步工具

## 概述

通过统一的 `shifu-cli.py` 管理 AI-Shifu 课程的完整生命周期：创建、查看、编辑、导入、发布。

## 课程目录结构

```
pipeline/mdf-courses/<course>/
  ├── README.md            # 课程元信息
  ├── system-prompt.md     # 课程级 system prompt（AI 引擎的角色设定和教学规范）
  ├── shifu-import.json    # 生成的导入文件
  ├── structure.json       # 章节结构（用于嵌套导入）
  └── lessons/
      ├── lesson-01.md     # MDF 提示词
      ├── lesson-02.md
      └── ...
```

### system-prompt.md

课程级提示词，定义 AI 引擎的角色、教学风格和交互规范。`build` 命令会自动读取并填入 `shifu.llm_system_prompt`。

**注意**：MDF 不需要写注释（`<!-- -->`），HTML 注释会被解析器直接丢弃，AI 引擎看不到。普通文本本身就是给 AI 的指令，直接写在 MDF 内容里即可。

## shifu-cli.py 用法

统一 CLI 工具，位于 `{skillDir}/scripts/shifu-cli.py`。

### 认证

首次使用需要登录，token 会保存到 `{skillDir}/.env`，后续命令自动复用：

```bash
python3 {skillDir}/scripts/shifu-cli.py login --phone 13800138000 --base-url https://app.ai-shifu.cn
```

也可以手动设置环境变量：
- `--base-url` 或 `.env` 中的 `SHIFU_BASE_URL`
- `--token` 或 `.env` 中的 `SHIFU_TOKEN`

**认证方式**：Cookie（`Cookie: token=<JWT>`），不是 Bearer。
**API 路径**：`/api/shifu`（不是 `/api/v1`）。

### 查询命令

```bash
# 列出所有课程
python3 {skillDir}/scripts/shifu-cli.py list

# 查看课程详情 + 大纲树
python3 {skillDir}/scripts/shifu-cli.py show <shifu_bid>

# 读取某节课的 MDF 内容
python3 {skillDir}/scripts/shifu-cli.py show <shifu_bid> <outline_bid>

# MDF 历史版本
python3 {skillDir}/scripts/shifu-cli.py history <shifu_bid> <outline_bid>

# 导出课程 JSON
python3 {skillDir}/scripts/shifu-cli.py export <shifu_bid> [-o file.json]
```

### 创建命令

```bash
# 创建空课程
python3 {skillDir}/scripts/shifu-cli.py create --name "课程标题" [--description "描述"]

# 添加单节课
python3 {skillDir}/scripts/shifu-cli.py add-lesson <shifu_bid> --name "课节名" --mdf-file lesson.md [--parent-bid <parent_bid>]
```

### 修改命令

```bash
# 更新课程元数据（名称、描述、系统提示词等）
python3 {skillDir}/scripts/shifu-cli.py update-meta <shifu_bid> [--name "..."] [--description "..."] [--system-prompt-file prompt.md]

# 更新单节课 MDF 内容（带乐观锁）
python3 {skillDir}/scripts/shifu-cli.py update-lesson <shifu_bid> <outline_bid> --mdf-file lesson.md

# 重命名课节
python3 {skillDir}/scripts/shifu-cli.py rename-lesson <shifu_bid> <outline_bid> --name "新名称"

# 重排课节顺序
python3 {skillDir}/scripts/shifu-cli.py reorder <shifu_bid> --order bid1,bid2,bid3
```

### 删除命令

```bash
# 删除某节课
python3 {skillDir}/scripts/shifu-cli.py delete-lesson <shifu_bid> <outline_bid>
```

### 批量导入

```bash
# 全量导入（平铺 JSON）
python3 {skillDir}/scripts/shifu-cli.py import <shifu_bid> --json-file course.json
python3 {skillDir}/scripts/shifu-cli.py import --new --json-file course.json

# 嵌套导入（章→节结构）
python3 {skillDir}/scripts/shifu-cli.py import <shifu_bid> --structure structure.json --lessons-dir ./lessons/
python3 {skillDir}/scripts/shifu-cli.py import --new --structure structure.json --lessons-dir ./lessons/

# 本地生成导入 JSON（不需要网络，自动创建章→节两级结构）
python3 {skillDir}/scripts/shifu-cli.py build --course-dir ./course-a/ [-o shifu-import.json] [--title "..."] [--chapter-name "..."]
# 若 course-dir 下存在 structure.json，则按其定义生成多章结构
```

### 状态管理

```bash
# 发布课程
python3 {skillDir}/scripts/shifu-cli.py publish <shifu_bid>

# 归档
python3 {skillDir}/scripts/shifu-cli.py archive <shifu_bid>

# 取消归档
python3 {skillDir}/scripts/shifu-cli.py unarchive <shifu_bid>
```

## Agent 引导流程

### 登录流程

当用户没有可用 token 时，agent 应引导用户完成 SMS 登录：

1. **询问手机号**：向用户索要 AI-Shifu 注册手机号
2. **发送验证码**：调用 `POST {base_url}/api/user/send_sms_code`，body: `{"mobile": "<phone>"}`
3. **等待验证码**：告知用户验证码已发送，请用户回复收到的验证码
4. **验证登录**：调用 `POST {base_url}/api/user/verify_sms_code`，body: `{"mobile": "<phone>", "sms_code": "<code>"}`
5. **获取 token**：从响应 `data` 字段获取 JWT token
6. **继续操作**：使用获取的 token 进行后续命令

示例 agent 对话：
```
Agent: 请告诉我你在 AI-Shifu 注册的手机号，我来帮你登录
User: 13800138000
Agent: 验证码已发送到 138****8000，请回复收到的验证码
User: 123456
Agent: 登录成功！开始操作课程...
```

**注意**：agent 执行时不要直接跑脚本的 `input()` 交互模式，而是通过 agent 对话引导用户，自行调用 API 获取 token 后再传给脚本。

### 典型工作流

**查看并更新单节课内容**：
```bash
shifu-cli.py list                               # 找到课程 BID
shifu-cli.py show <shifu_bid>                    # 查看大纲树，找到目标课节
shifu-cli.py show <shifu_bid> <outline_bid>      # 读取当前 MDF 内容
# ... 编辑本地 MDF 文件 ...
shifu-cli.py update-lesson <shifu_bid> <outline_bid> --mdf-file updated.md
```

**从本地目录完整部署**：
```bash
shifu-cli.py build --course-dir ./course-a/ --title "课程名"
shifu-cli.py import --new --json-file ./course-a/shifu-import.json
shifu-cli.py publish <shifu_bid>
```

## AI-Shifu 导入 JSON 格式

```json
{
  "version": "1.0",
  "shifu": {
    "shifu_bid": "<UUID>",
    "title": "课程标题",
    "description": "描述",
    "keywords": "关键词",
    "llm": "",
    "llm_temperature": 0,
    "llm_system_prompt": "<system-prompt.md 内容>",
    "ask_enabled_status": 5101,
    "price": 0.0
  },
  "outline_items": [
    {
      "outline_item_bid": "<UUID>",
      "title": "课节标题",
      "type": 401,
      "parent_bid": "",
      "position": "0",
      "content": "<MDF 内容>"
    }
  ],
  "structure": { "bid": "<shifu_bid>", "type": "shifu", "children": [...] }
}
```

### 关键字段
- `llm_system_prompt`：课程级 AI 角色设定（来自 system-prompt.md）
- `type: 401`：普通课节
- `parent_bid`：留空=章（顶级容器），填写=节（子节点，MDF 内容在此层级）
- `content`：MDF 提示词内容（核心）
- `ask_enabled_status: 5101`：允许用户提问

## 验证

操作后检查：
1. 管理后台：`https://app.ai-shifu.cn/shifu/<shifu_bid>`
2. 预览：`https://app.ai-shifu.cn/c/<shifu_bid>?preview=true`
3. 逐节检查 MDF 内容、变量采集、交互逻辑
