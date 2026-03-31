- The base include set is the scoped element `cloud.backend` plus its **direct children**; `include *` in a scoped view does not mean the whole model, and it also does not recurse to every descendant unless deeper nesting becomes needed by view expansion rules.
- From that scoped base, neighboring and derived visibility can still appear: incoming and outgoing relationships for the included elements can pull in external source/target elements as needed, and any implied/derived relationships produced by the scoped hierarchy may also be rendered if they connect visible elements.

```likec4
view backend of cloud.backend {
  include *
  include -> *
  include * ->
}
```