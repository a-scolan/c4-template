For an upload journey “step by step” with highlighted critical elements, combine two views:

1. **Dynamic view** for sequence clarity
   - Show the exact flow: user -> web app -> API -> queue/worker -> storage/database
   - Include key branches (success/failure/retry) only if they are essential

2. **Static view styling** for emphasis
   - Apply tags to critical elements (e.g., API, queue, worker, data store)
   - Use targeted styles/colors in the relevant static view to highlight those tagged elements
   - Keep non-critical nodes muted to preserve readability

This gives you clear temporal behavior (dynamic) plus durable visual emphasis (styled static view).Use a **Dynamic view** for the step-by-step upload journey, plus optional style/tag rules for critical highlighting.

Recommended LikeC4 approach:
1. Model actors/containers/components involved in upload.
2. Add a **dynamic view** named like `upload_journey`.
3. Encode each interaction in sequence order.
4. Tag critical nodes/edges (e.g., `#critical`) and color them via styles.

Example skeleton:

```likec4
model {
  user = person "User"

  platform = system "Platform" {
    web = container "Web App"
    uploadApi = container "Upload API"
    storage = container "Object Storage"
    scanner = container "Malware Scanner"
    notifier = container "Notification Service"
  }

  user -> platform.web "Uploads file"
  platform.web -> platform.uploadApi "POST /upload"
  platform.uploadApi -> platform.storage "Store blob" #critical
  platform.uploadApi -> platform.scanner "Scan file" #critical
  platform.uploadApi -> platform.notifier "Emit upload event"
}

views {
  dynamic view upload_journey {
    title "Upload Journey"

    user -> platform.web "1. Select and submit file"
    platform.web -> platform.uploadApi "2. Send upload request"
    platform.uploadApi -> platform.storage "3. Persist file"
    platform.uploadApi -> platform.scanner "4. Run security scan"
    platform.uploadApi -> platform.notifier "5. Publish completion event"
    platform.web -> user "6. Show success/failure"
  }
}

styles {
  element.tag "critical" {
    color red
  }
  relationship.tag "critical" {
    color red
  }
}
```

Why this is best:
- Dynamic view captures **ordered behavior**.
- Tags + styles provide **clear visual emphasis** on critical parts.
- Keeps architecture and flow documentation consistent in one model.