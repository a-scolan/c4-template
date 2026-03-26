Use the exact relationship identity when extending. If multiple relations share endpoints, kind/title are required to disambiguate.

Given `frontend -[async]-> api "streams"`, the correct extension is:

```likec4
model {
  extend frontend -[async]-> api "streams" {
    metadata { qos "high" }
  }
}
```