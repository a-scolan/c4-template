# Identity Provider + Portal API — Direct Declarations

**Declarations only, no arrows yet.**

```likec4
model {
  // Third-party identity provider — Context level (C1)
  identityProvider = System_External 'Identity Provider' {
    technology 'SAML 2.0 / OIDC'
    description 'External identity and access management platform responsible for authentication and SSO token issuance.'
  }

  portalSystem = System_New 'Portal System' {

    // Internal portal API — Container level (C2)
    portalApi = Container_Api 'Portal API' {
      technology 'Node.js, Fastify'
      description 'Core backend API for the portal, enforces authorization and proxies identity tokens from the identity provider.'
    }

  }
}
```

**Kinds used:**
- `System_External` — declared kind for any third-party/external platform
- `Container_Api` — declared kind for any internal API container

Both come from the shared spec. No new kinds required.

**Next step:** when relationships are needed, use **`create-relationship`**.
