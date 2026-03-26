That relationship is invalid as a modeling pattern: parent-child hierarchy already expresses containment; do not model synthetic "contains traffic" from parent to child.

Minimal corrected pattern:

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    frontend = container 'Frontend'

    frontend -> backend 'Calls API'
  }
}
```