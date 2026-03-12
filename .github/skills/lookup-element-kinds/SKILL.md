---
name: lookup-element-kinds
description: Use when you are unsure of the exact kind or relationship name in the active workspace, especially when similar spellings exist or you need to distinguish logical-model taxonomy from deployment taxonomy.
---

# Verify LikeC4 Element Kinds and Relationship Types

## Overview

Use this skill to **confirm exact names from the active workspace**, not to guess from memory or English labels. The source of truth is the current LikeC4 project summary plus the shared specification files.

The goal is not merely to list kinds — it is to answer three questions safely:
1. **What is the exact spelling?**
2. **Is it a logical-model kind or a deployment kind?**
3. **How do I verify it before writing model code?**

## When to Use

- Choosing between similar spellings such as `Container_Api` vs `Container_API`
- Verifying whether a relationship kind belongs to the logical model or deployment
- Looking up nearby valid kinds for a node, zone, infrastructure element, or container
- Checking the active workspace before creating or editing elements/relationships

## Verification Workflow

1. **Read the active project summary** — use `read-project-summary` to see the current element kinds and relationship kinds.
2. **Check the relevant shared spec** — container/system kinds in `projects/shared/spec-context.c4` or `spec-containers.c4`; deployment kinds in `spec-deployment.c4`.
3. **Resolve close spellings by exact match** — trust the declared identifier, not the most readable English expansion.
4. **Classify the interaction** — logical model vs deployment. This decides which relationship taxonomy is even legal.
5. **Only then write the model code** — if still uncertain, stop and verify again instead of inventing a kind.

## Quick Reference

| Question | Source of truth | Typical resolution |
|----------|-----------------|--------------------|
| Exact container kind? | `read-project-summary`, `spec-containers.c4` | Prefer the declared subtype such as `Container_Api` |
| Exact infrastructure kind? | `read-project-summary`, `spec-deployment.c4` | Trust the repository spelling, e.g. `Infra_Fw` |
| Logical vs deployment relationship? | project summary + modeling context | Logical model uses `calls/reads/writes/async/uses`; deployment uses `https/tcp/sql/...` |
| Two names look similar? | exact declared identifier | Reject the lookalike and cite the real one |

## Common Exact Checks in This Workspace

These examples are useful because they are easy to get wrong:

| Intent | Exact declared name | Lookalike to reject |
|--------|---------------------|---------------------|
| API container | `Container_Api` | `Container_API` |
| Firewall infrastructure | `Infra_Fw` | `Infra_Firewall` |
| VM deployment node | `Node_Vm` | `Node_VM` |
| Database container | `Container_Database` | ad-hoc names like `Container_DB` |

## Logical Model vs Deployment Taxonomy

### Logical model relationships

Use these for normal application behavior:

`calls`, `async`, `reads`, `writes`, `uses`

### Deployment relationships

Use these only for deployment-side infrastructure edges:

`http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`

If the interaction belongs in the logical model, keep the logical kind and put the protocol in `technology`, for example `technology 'HTTPS'` or `technology 'HTTP/8080'`.

## Example Verification Pattern

```likec4
// 1. Confirm the exact kind from the active workspace
api = Container_Api 'REST API' {
  technology 'Node.js'
}

// 2. Use logical-model relationship kinds for app behavior
api -[calls]-> externalProvider 'Authenticates user' {
  technology 'HTTPS'
}

// 3. Use data-access relationships for stores
api -[reads]-> primaryDatabase 'Fetches records'
api -[writes]-> primaryDatabase 'Stores records'
```

## Common Mistakes

❌ **Guessing from English labels** — `Container_API`, `Infra_Firewall`, and `Node_VM` may feel natural but are not the declared identifiers here

❌ **Using a generic base kind too early** — `Container` exists, but if a more specific declared subtype fits, use it

❌ **Inventing relationship kinds** — `query`, `invokes`, `triggers`, and other ad-hoc kinds are invalid unless declared in the spec

❌ **Mixing model and deployment taxonomies** — `https` is not a logical-model relationship kind for normal application traffic; `calls` is not a deployment edge kind

## Handoffs

- Need to create the element once the kind is known? Use `create-element`
- Need to choose the relationship after confirming taxonomy? Use `create-relationship`
- Need to re-check workspace context first? Use `understand-project-structure`
