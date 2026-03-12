Use three separate layers instead of one overloaded view:

1. **Structural companion view**: create a small static view that frames the upload scope.

```likec4
views 'C2' {
  view upload_scope {
    title 'Upload Scope'

    include user
    include mySystem.webapp
    include mySystem.api
    include mySystem.database
    include emailService

    rank source { user }
    rank sink { mySystem.database, emailService }
  }
}
```

2. **Temporal flow**: capture the step-by-step upload journey in a dedicated dynamic or sequence view, separate from the structural view.
3. **Visual emphasis**: apply colors in a later styling/customization pass so critical elements stand out without mixing presentation rules into the journey logic.

Keep the structural view small and stable; let the time-ordered narrative and color treatment live in their own follow-up artifacts.
