---
name: create-relationship
description: Create typed relationships with FQN, proper kinds (calls/async/reads/writes), descriptive labels, and no return relationships.
---

# Create LikeC4 Relationship

Use this skill when connecting elements in model or deployment files.

## Requirements

1. **Check for duplicates (RECOMMENDED):** Use LikeC4 MCP `find-relationships` to verify no duplicate relationships exist
2. **Use FQN:** Fully qualified names for nested elements (e.g., `mySystem.api`)
3. **Typed relationships:** Always specify relationship kind
   - Model: `calls`, `async`, `reads`, `writes`, `uses`
   - Deployment: `http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`
4. **Label:** Required descriptive text
5. **No returns:** Never create reverse relationships (responses are implicit)
6. **Optional description:** Add block with details if needed

## Example

```likec4
mySystem.api -[calls]-> externalService 'Fetches data' {
  description 'HTTPS REST API with OAuth 2.0'
}
```

## Anti-patterns

```likec4
❌ api -> service 'Calls'                    // Missing relationship kind
❌ mySystem.api -[invokes]-> service         // Invalid relationship kind
❌ client -[calls]-> server 'Request'
   server -[calls]-> client 'Response'      // No return relationships!
```
