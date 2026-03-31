1. `extend api -[async]-> service 'GetData' { metadata { timeout '5s' } }` — **correct**
2. `extend api -[async]-> service { metadata { timeout '5s' } }` — **ambiguous**
3. `extend api -> service 'GetData' { metadata { timeout '5s' } }` — **ambiguous**

```likec4
extend api -[async]-> service 'GetData' {
  metadata {
    timeout '5s'
  }
}
```