---
name: ai-shifu-course-manager
description: Deploy, manage, and sync MDF course files to the AI-Shifu platform. Use this skill whenever the user mentions AI-Shifu courses, MDF deployment, lesson importing, course publishing, shifu-cli, or wants to create/update/export courses on AI-Shifu — even if they don't explicitly say "deploy". Also triggers for bulk lesson imports, course lifecycle management (publish, archive), or syncing local MDF files to a remote platform.
---

# AI-Shifu Course Manager

Manage the full lifecycle of AI-Shifu courses through `shifu-cli.py`: create, query, edit, import, publish, and archive.

## Course Directory Structure

```
<course>/
  ├── README.md            # Course metadata (title, description)
  ├── system-prompt.md     # Course-level system prompt (AI role and teaching style)
  ├── shifu-import.json    # Generated import file
  ├── structure.json       # Chapter structure (for nested imports)
  └── lessons/
      ├── lesson-01.md     # MDF lesson file
      ├── lesson-02.md
      └── ...
```

### system-prompt.md

Defines the AI engine's role, teaching style, and interaction rules at the course level. The `build` command reads this file and populates `shifu.llm_system_prompt` automatically.

Note: MDF files do not support HTML comments (`<!-- -->`). The parser discards them entirely, so the AI engine never sees them. Write instructions as plain text directly in the MDF content.

## CLI Reference

All commands use `{skillDir}/scripts/shifu-cli.py`. Prefix every call with:

```bash
python3 {skillDir}/scripts/shifu-cli.py <command>
```

### Authentication

Run login once — the token persists in `{skillDir}/.env` for subsequent commands:

```bash
login --phone 13800138000 --base-url https://app.ai-shifu.cn
```

Alternatively, set environment variables or CLI flags:
- `--base-url` or `SHIFU_BASE_URL` in `.env`
- `--token` or `SHIFU_TOKEN` in `.env`

Authentication uses Cookie (`Cookie: token=<JWT>`), not Bearer. The API prefix is `/api/shifu` (not `/api/v1`).

### Query Commands

```bash
list                                          # List all courses
show <shifu_bid>                              # Show course details + outline tree
show <shifu_bid> <outline_bid>                # Read a lesson's MDF content
history <shifu_bid> <outline_bid>             # MDF revision history
export <shifu_bid> [-o file.json]             # Export course as JSON
```

### Create Commands

```bash
create --name "Title" [--description "Desc"]                              # Create empty course
add-lesson <shifu_bid> --name "Name" --mdf-file lesson.md [--parent-bid]  # Add single lesson
```

### Update Commands

```bash
update-meta <shifu_bid> [--name "..."] [--description "..."] [--system-prompt-file prompt.md]
update-lesson <shifu_bid> <outline_bid> --mdf-file lesson.md    # Uses optimistic locking
rename-lesson <shifu_bid> <outline_bid> --name "New Name"
reorder <shifu_bid> --order bid1,bid2,bid3
```

`update-lesson` fetches the current revision before saving. If another user modified the lesson since you last read it, the server returns a conflict — this prevents accidental overwrites in collaborative editing.

### Delete Commands

```bash
delete-lesson <shifu_bid> <outline_bid>
```

### Bulk Import

```bash
# Flat JSON import
import <shifu_bid> --json-file course.json
import --new --json-file course.json

# Nested import (chapter → lesson structure)
import <shifu_bid> --structure structure.json --lessons-dir ./lessons/
import --new --structure structure.json --lessons-dir ./lessons/

# Local build (offline, generates shifu-import.json)
build --course-dir ./course-a/ [-o shifu-import.json] [--title "..."] [--chapter-name "..."]
```

The `build` command works entirely offline — it reads local MDF files and produces `shifu-import.json` without any network calls. If `structure.json` exists in the course directory, it generates a multi-chapter structure; otherwise it creates a single chapter containing all lessons.

### State Management

```bash
publish <shifu_bid>       # Publish course (makes it live)
archive <shifu_bid>       # Archive course
unarchive <shifu_bid>     # Restore archived course
```

## Agent Guidance

### Login Flow

When no valid token is available, guide the user through SMS login interactively:

1. Ask the user for their AI-Shifu registered phone number
2. Send verification code: `POST {base_url}/api/user/send_sms_code` with `{"mobile": "<phone>"}`
3. Ask the user to reply with the code they received
4. Verify: `POST {base_url}/api/user/verify_sms_code` with `{"mobile": "<phone>", "sms_code": "<code>"}`
5. Extract the JWT token from `response.data`
6. Save the token and proceed with the requested operation

Do not run the CLI's interactive `input()` mode. Instead, handle the login conversation yourself and pass the token to the CLI via `--token` or by writing it to `.env`.

### Common Workflows

**View and update a single lesson:**
```bash
list                                              # Find the course BID
show <shifu_bid>                                  # Browse outline tree
show <shifu_bid> <outline_bid>                    # Read current MDF content
# ... edit the local MDF file ...
update-lesson <shifu_bid> <outline_bid> --mdf-file updated.md
```

**Full deployment from local directory:**
```bash
build --course-dir ./course-a/ --title "Course Name"
import --new --json-file ./course-a/shifu-import.json
publish <shifu_bid>
```

## Import JSON Format

```json
{
  "version": "1.0",
  "shifu": {
    "shifu_bid": "<UUID>",
    "title": "Course Title",
    "description": "Description",
    "keywords": "keywords",
    "llm": "",
    "llm_temperature": 0,
    "llm_system_prompt": "<content from system-prompt.md>",
    "ask_enabled_status": 5101,
    "price": 0.0
  },
  "outline_items": [
    {
      "outline_item_bid": "<UUID>",
      "title": "Lesson Title",
      "type": 401,
      "parent_bid": "",
      "position": "0",
      "content": "<MDF content>"
    }
  ],
  "structure": { "bid": "<shifu_bid>", "type": "shifu", "children": [] }
}
```

Key fields:
- `llm_system_prompt`: Course-level AI role definition (from system-prompt.md)
- `type: 401`: Regular lesson node
- `parent_bid`: Empty string = chapter (top-level container); non-empty = lesson (child node with MDF content)
- `content`: The MDF prompt content (this is the core teaching material)
- `ask_enabled_status: 5101`: Enables learner questions

## Verification

After any operation, verify the result:
1. Admin console: `https://app.ai-shifu.cn/shifu/<shifu_bid>`
2. Preview: `https://app.ai-shifu.cn/c/<shifu_bid>?preview=true`
3. Check each lesson's MDF content, variable collection, and interaction logic
