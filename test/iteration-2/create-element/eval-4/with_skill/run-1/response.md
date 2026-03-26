# Third-Party Identity Provider + Internal Portal API

**Most direct declarations, no relationships yet.**

## Identity Provider (External System — C1)

```likec4
model {
  identityProvider = System_External 'Identity Provider' {
    technology 'OIDC / OAuth 2.0'
    description 'Third-party identity and access management service handling authentication and token issuance.'
  }
}
```

## Portal API (Internal Container — C2)

```likec4
model {
  portalSystem = System_New 'Portal System' {

    portalApi = Container_Api 'Portal API' {
      technology 'Node.js, Express'
      description 'Backend API for the user portal, serving authenticated requests and delegating auth to the identity provider.'
    }

  }
}
```

Both use exact shared kinds: `System_External` for the third-party platform, `Container_Api` for the internal API container. No custom kinds needed.

When you are ready to add the relationship, use **`create-relationship`**.
