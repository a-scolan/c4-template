(1) correct
(2) ambiguous
(3) wrong

```likec4
extend api -[async]-> service 'GetData' {
  metadata { timeout '5s' }
}
```