Valid as written.

A view declared with `extends <parentViewId>` inherits the scope (`of` target) from the parent view, so repeating `of cloud.backend` is not required. The child view starts with everything the parent rendered and can then add, exclude, or style elements on top. Because `backend-detail` extends `backend-overview`, its implicit scope is already `cloud.backend`, and `include api` is resolved within that scope.

Smallest final snippet that also adds incoming relationships to `cloud.backend`:

```likec4
view backend-detail extends backend-overview {
  include api
  include -> cloud.backend
}
```

`include -> cloud.backend` pulls in all elements that have a direct relationship pointing **to** `cloud.backend`, together with those relationship edges, making all callers visible in the view.
