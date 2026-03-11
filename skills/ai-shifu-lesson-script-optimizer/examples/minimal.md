# Minimal Example

## Input Payload (example)

```json
{
  "existing_mdf_script": "## Objective\nUnderstand retry policy.\n---\n?[%{{answer}} yes | no]\n---\nGreat job.",
  "source_course_material": "Learner must differentiate transient vs permanent failure and choose a matching retry stop rule.",
  "optimization_constraints": {
    "max_interactions": 4,
    "require_branching_feedback": true
  },
  "course_profile": {
    "audience_level": "beginner"
  }
}
```

## Output Snapshot (example)

```json
{
  "risk_and_issue_report": {
    "overall_risk": "medium",
    "blocking_issues": ["interaction_no_branching"],
    "suggestions": ["add explicit stop-condition task"]
  },
  "change_list": [
    {
      "issue_class": "interaction_no_branching",
      "change": "branch feedback by learner option and add next-step action"
    }
  ]
}
```

```md
## Objective
Differentiate transient and permanent failures before choosing retry policy.
---
?[%{{failure_type}} transient failure | permanent failure]
---
If {{failure_type}} is transient, apply bounded retries with backoff.
If {{failure_type}} is permanent, stop retries and open a corrective task.
```

## Acceptance Notes

- Syntax stays runnable after edits.
- Coverage and meaning are closer to source material.
- Interaction feedback is clearly branched.
