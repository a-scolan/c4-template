Use `create-element` for the element declarations only:

- `virusScanProvider`: model it as `System_External`
- `scanApi`: model it with an existing internal kind such as `Container_Api`

Then hand off the other parts to the right skills:

- Arrows / connections: `create-relationship`
- C2 view: `design-view`

So the split is: elements with `create-element`, arrows with `create-relationship`, and the container view with `design-view`.