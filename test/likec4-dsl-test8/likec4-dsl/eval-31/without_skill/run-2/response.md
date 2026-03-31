(1) correct
(2) ambiguous
(3) ambiguous

```likec4
extend api -[async]-> service 'GetData' {
  metadata {
    timeout '5s'
  }
}
```