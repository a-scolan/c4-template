# Creating `Container_UploadOrchestrator` — Not Recommended

**Short answer:** Do not create this kind. The **shared-spec-first rule** says to reuse existing kinds before inventing new ones.

## The Rule

The skill is explicit:
> Invent `Container_UploadOrchestrator` for a single service when `Container_Api` or another declared kind already fits → **Bad decision**.

## Checklist Before Adding Any New Kind

1. Open `projects/shared/SPEC_CHEATSHEET.md` and review all declared container kinds.
2. Open `projects/shared/spec-containers.c4` to see exact kind names and their intent.
3. Ask whether `Container_Api`, `Container_Queue`, or another kind communicates the responsibility clearly.
4. If none fit, check whether this generalizes enough to go in shared specs rather than as a project-local kind.

## Recommendation

Use `Container_Api` with a descriptive title and description. Kind names describe structural shape; element names and descriptions describe specific responsibility:

```likec4
uploadOrchestrator = Container_Api 'Upload Orchestrator' {
  technology 'Node.js'
  description 'Orchestrates upload steps: validates files, persists to object storage, and triggers processing.'
}
```

A new kind is only a last resort when no existing shared kind fits the structural role.
