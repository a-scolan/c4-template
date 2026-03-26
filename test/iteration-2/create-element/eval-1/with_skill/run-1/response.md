# Should I Create `Container_UploadOrchestrator`?

**No** — this would violate the **shared-spec-first rule**.

## The Rule

> Prefer an existing shared kind over a one-off local kind.

Creating `Container_UploadOrchestrator` for a single service is a bad decision when an existing kind already covers the responsibility. The skill explicitly lists this as an example of what **not** to do.

## What to Do First

1. **Check `projects/shared/SPEC_CHEATSHEET.md`** — lists all declared container kinds.
2. **Check `projects/shared/spec-containers.c4`** — confirms exact spellings and any descriptions.
3. Ask: does `Container_Api` (or another existing kind) communicate this service's responsibility clearly enough with a good name and description?

## Conclusion

For a single upload service, `Container_Api` almost certainly fits. Give it a clear title and description instead:

```likec4
model {
  uploadSystem = System_New 'Upload System' {

    uploadOrchestrator = Container_Api 'Upload Orchestrator' {
      technology 'Node.js, Express'
      description 'Coordinates file upload steps: validation, storage, and downstream notification.'
    }

  }
}
```

Only propose a new kind if **no existing shared kind** covers the structural role — and even then, the new kind should go into `projects/shared/`, not as a local one-off.
