Use a three-part approach.

1. Keep this work limited to a companion structural view.
2. Use `create-sequence-view` for the step-by-step upload journey.
3. Use `customize-view` for colors and critical-element highlighting.

A good structural companion is a static C2 view that frames the main upload participants:

```likec4
views 'C2' {
  view upload_structure {
    title 'Upload Structure'

    include user
    include mySystem
    include mySystem.webapp
    include mySystem.api
    include mySystem.database
    include emailService
  }
}
```

That gives you the structural anchor. The temporal flow itself belongs in `create-sequence-view`, and the visual emphasis belongs in `customize-view`. Keeping those concerns separate makes the result much cleaner: one view explains structure, one explains sequence, and one applies styling.