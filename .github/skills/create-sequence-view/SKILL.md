---
name: create-sequence-view
description: Create sequence views showing temporal flows and user interactions. Uses plain arrows with descriptive labels (no relationship kinds).
---

# Create Dynamic Sequence View

Use this skill when documenting use case flows and interactions.

## Requirements

1. **Use `dynamic view`** with descriptive ID
2. **No relationship kinds:** Use plain `->` not `-[kind]->`
3. **Step labels:** Add descriptive text for each interaction
4. **User-to-system flow:** Start with actor, show system responses
5. **Temporal order:** Steps execute top-to-bottom

## Example

```likec4
dynamic view sequence_upload {
  title 'Use Cases / Document Upload Flow'
  
  user -> mySystem.webapp 'Opens upload form'
  mySystem.webapp -> mySystem.api 'POST /upload'
  mySystem.api -> mySystem.storage 'Store file'
  mySystem.api -> mySystem.queue 'Queue processing job'
  mySystem.queue -> mySystem.worker 'Execute job'
  mySystem.worker -> mySystem.database 'Update metadata'
}
```
