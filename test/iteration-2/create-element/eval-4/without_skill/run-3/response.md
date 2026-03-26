Start with just the two element declarations, no relationships yet:

```likec4
model {
  identityProvider = externalSystem "Identity Provider"
  portalApi = container "Portal API"
}
```

If `portalApi` must be nested, place it inside your existing internal system block.