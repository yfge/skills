---
name: ai-shifu-course-manager
description: Deploy, manage, and sync MDF course files to the AI-Shifu platform. Use this skill whenever the user mentions AI-Shifu courses, MDF deployment, lesson importing, course publishing, shifu-cli, or wants to create/update/export courses on AI-Shifu — even if they don't explicitly say "deploy". Also triggers for bulk lesson imports, course lifecycle management (publish, archive), or syncing local MDF files to a remote platform.
---

# AI-Shifu Course Manager

Manage the full lifecycle of AI-Shifu courses through `shifu-cli.py`: create, query, edit, import, publish, and archive.

## Course Directory Structure

```
<course>/
  ├── README.md            # Course metadata (title from first heading)
  ├── system-prompt.md     # Course-level system prompt (AI role and teaching style)
  ├── shifu-import.json    # Generated import file (output of build)
  ├── structure.json       # Chapter structure (optional, for multi-chapter courses)
  └── lessons/
      ├── lesson-01.md     # MDF lesson file (must match lesson-*.md pattern)
      ├── lesson-02.md
      └── ...
```

### Lesson Files

Lesson files must be named `lesson-*.md` (e.g., `lesson-01.md`, `lesson-02.md`). Files that do not match this pattern are ignored by the `build` command.

### system-prompt.md

Defines the AI engine's role, teaching style, and interaction rules at the course level. The `build` command reads this file and populates `shifu.llm_system_prompt` automatically.

Note: MDF files do not support HTML comments (`<!-- -->`). The parser discards them entirely, so the AI engine never sees them. Write instructions as plain text directly in the MDF content.

### structure.json

Defines multi-chapter course structure. If this file exists, `build` uses it to organize lessons into chapters; otherwise all lessons are placed under a single auto-generated chapter.

Schema:

```json
{
  "chapters": [
    {
      "title": "Chapter Title",
      "lessons": [
        {"file": "lesson-01.md", "title": "Lesson Title"},
        {"file": "lesson-02.md"}
      ]
    }
  ]
}
```

Field reference:
- `chapters[].title` (required): Chapter display name
- `chapters[].lessons[]` (required): Array of lesson objects
- `chapters[].lessons[].file` (required): Filename in the `lessons/` directory, must match a `lesson-*.md` file
- `chapters[].lessons[].title` (optional): Lesson display name. If omitted, auto-extracted from MDF content (`lesson_title: ...` line) or derived from filename

## CLI Reference

All commands use `{skillDir}/scripts/shifu-cli.py`. Prefix every call with:

```bash
python3 {skillDir}/scripts/shifu-cli.py <command>
```

### Authentication

Run login once — the token persists in `{skillDir}/.env` for subsequent commands:

```bash
# Step 1: Send SMS verification code
login --phone 13800138000 --region cn

# Step 2: Complete login with the code
login --phone 13800138000 --region cn --sms-code 123456
```

Region options: `cn` (中国大陆, maps to `https://app.ai-shifu.cn`) or `global` (非中国大陆, maps to `https://app.ai-shifu.com`). You can also use `--base-url` to override the URL directly.

Alternatively, set environment variables or CLI flags:
- `--base-url` or `SHIFU_BASE_URL` in `.env`
- `--token` or `SHIFU_TOKEN` in `.env`

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
add-chapter <shifu_bid> --name "Chapter Name"                              # Create top-level chapter
add-lesson <shifu_bid> --name "Name" --mdf-file lesson.md --parent-bid <chapter_bid>
                                                                          # Add lesson under a chapter
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

The `build` command works entirely offline — it reads local MDF files and produces `shifu-import.json` without any network calls.

Build behavior:
- **Course title** resolution order: `--title` CLI arg → first heading in `README.md` → directory name
- **Chapter structure**: if `structure.json` exists, generates multi-chapter structure per its definition; otherwise creates a single chapter (named via `--chapter-name` or defaults to course title) containing all `lesson-*.md` files in sorted order
- **Lesson title** resolution order: `title` field in `structure.json` → `lesson_title: ...` line in MDF content → filename derived (e.g., `lesson-01.md` → "Lesson 01")

### State Management

```bash
publish <shifu_bid>       # Publish course (makes it live)
archive <shifu_bid>       # Archive course
unarchive <shifu_bid>     # Restore archived course
```

## Agent Guidance

### Login Flow

When no valid token is available, guide the user through login:

1. Ask the user to choose their region:
   - 1: 中国大陆用户
   - 2: 非中国大陆用户
2. **If the user chooses 非中国大陆用户**: CLI login is not supported for this region. Tell the user to log in manually at `https://app.ai-shifu.com`, copy their token from the browser, and set it via `--token` or by adding `SHIFU_TOKEN=<token>` and `SHIFU_BASE_URL=https://app.ai-shifu.com` to `{skillDir}/.env`. Then stop — do not proceed with the SMS flow.
3. **If the user chooses 中国大陆用户**: continue with the SMS login flow below.
4. Ask for their registered phone number
5. Send SMS code:
   `python3 {skillDir}/scripts/shifu-cli.py login --phone <phone> --region cn`
6. Ask the user for the verification code they received
7. Complete login:
   `python3 {skillDir}/scripts/shifu-cli.py login --phone <phone> --region cn --sms-code <code>`
8. Token is automatically saved — proceed with the requested operation

Always use CLI commands. Never make raw HTTP/API calls directly.

### Common Workflows

**First upload (no course/chapter exists yet):**
```bash
create --name "Course Title" --description "..."            # Create the course
add-chapter <shifu_bid> --name "Chapter 1"                   # Create a chapter
add-lesson <shifu_bid> --name "Lesson 1" --mdf-file lesson.md --parent-bid <chapter_bid>
show <shifu_bid>                                              # Verify structure
```

Rule: when the user first asks to upload a lesson script, do not write into an existing placeholder node. Create the course, create a chapter, then create the lesson under that chapter.

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
- `parent_bid`: Empty string = chapter (top-level container); non-empty = lesson (child node with MDF content). Use `add-chapter` to create chapters, then pass the chapter BID as `--parent-bid` when creating lessons
- `content`: The MDF prompt content (this is the core teaching material)
- `ask_enabled_status: 5101`: Enables learner questions

## Verification

After any operation, verify the result:
1. Admin console: `https://app.ai-shifu.cn/shifu/<shifu_bid>`
2. Preview: `https://app.ai-shifu.cn/c/<shifu_bid>?preview=true`
3. Check each lesson's MDF content, variable collection, and interaction logic
