## Named deployment instances

Use `IDENTIFIER = instanceOf ELEMENT_ID` inside the deployment node. Each name must be unique within its parent node.

```likec4
deployment {
  vm appVm {
    apiBlue  = instanceOf cloud.api
    apiGreen = instanceOf cloud.api
  }
}
```

**Key points:**

- `apiBlue` and `apiGreen` are the distinct identifiers for each instance. They can be referenced by FQN (`appVm.apiBlue`, `appVm.apiGreen`) in deployment views or relationships.
- Both are instances of the same logical element `cloud.api`, but they are independent deployment nodes — useful for blue/green deployments, replicas, or canary scenarios.
- Using plain `instanceOf cloud.api` twice (without an identifier) creates two *anonymous* instances, which cannot be individually referenced or styled. That form is rejected by the prompt.
- Optional per-instance properties (`title`, `technology`, tags, `metadata`) can be added inside each instance body if the instances need to differ in their descriptions.

```likec4
deployment {
  vm appVm {
    apiBlue = instanceOf cloud.api {
      title "API — Blue slot"
      #blue
    }
    apiGreen = instanceOf cloud.api {
      title "API — Green slot"
      #green
    }
  }
}
```
