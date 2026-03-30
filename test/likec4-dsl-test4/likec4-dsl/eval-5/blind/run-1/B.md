Use `IDENTIFIER = instanceOf ELEMENT_ID` for each named instance inside the deployment node:

```likec4
deployment {
  vm appVm {
    apiBlue  = instanceOf cloud.api
    apiGreen = instanceOf cloud.api
  }
}
```

Both `apiBlue` and `apiGreen` are distinct, named deployed instances of the same logical element `cloud.api` inside a single `vm` node. They receive separate identifiers (FQNs: `appVm.apiBlue` and `appVm.apiGreen`), which lets you reference, relate, and style them independently in deployment views.

The anonymous form — two bare `instanceOf cloud.api` lines without an identifier — is invalid in LikeC4 if used more than once in the same scope because the instance has no assignable name to disambiguate it. The named form is the only way to have multiple instances of the same logical element coexist in one deployment node.
