# Identity Provider + Portal API

Here are the minimal declarations, relationships excluded as requested.

```likec4
model {
  identityProvider = System_External 'Identity Provider' {
    technology 'OIDC, OAuth 2.0'
    description 'Third-party identity platform that issues access tokens and manages user authentication.'
  }

  portalSystem = System_New 'Portal System' {

    portalApi = Container_Api 'Portal API' {
      technology 'Node.js, Express'
      description 'Internal portal backend API; validates tokens issued by the identity provider and serves portal data.'
    }

  }
}
```

**Kind selection:**
- `System_External` — correct kind for any external/vendor system at context level
- `Container_Api` — correct kind for an internal API container under a system

Both are from the shared spec — no new kinds invented.
