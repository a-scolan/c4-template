---
name: lookup-element-kinds
description: Use when creating elements or relationships and you need to validate kind names, discover available types, or check specification consistency.
---

# LikeC4 Element Kinds and Relationship Types Reference

## Overview

Quick reference listing the element kinds and relationship kinds currently declared in this template's shared specifications (`projects/shared/spec-*.c4`). Use it as a fast lookup when creating elements or validating relationship types.

## When to Use

- Verifying an element kind name before creating an element (e.g., `Container_Api` vs `Container_API`)
- Discovering available kinds when the shared spec isn’t open in the editor
- Validating a relationship kind (e.g., confirming `async` exists for model relationships)
- Checking if a deployment relationship kind (`https`, `tcp`, `amqp`) is valid

**Always confirm with MCP:** Use `read-project-summary` to validate the current shared spec in the active workspace. This list is a quick reference and may evolve.

## Quick Reference

**Keywords:** Actor, System, Container, Component, Zone, Node, Infrastructure, relationship kinds, type validation, specification

## Actors (C1)

`Actor`, `Actor_Person`, `Actor_Staff`, `Actor_Admin`

## Systems (C1)

`System_Existing`, `System_New`, `System_Legacy`, `System_External`

## Containers (C2)

`Container`, `Container_ReverseProxy`, `Container_Waf`, `Container_Browser`, `Container_MobileApp`, `Container_Spa`, `Container_Webapp`, `Container_Api`, `Container_Api_Geo`, `Container_Queue`, `Container_Database`, `Container_DatabaseGeo`, `Container_ObjectStorage`, `Container_Directory`, `Container_Mailserver`, `Container_Loadbalancer`, `Container_DataServer`, `Container_FileServer`, `Container_ProcessingServer`, `Container_ExchangeServer`, `Container_IamServer`, `Container_WebServer`, `Container_ApplicationServer`

## Components (C3)

`Component`

## Deployment Zones

`Zone`, `Zone_Internet`, `Zone_Vlan`, `Zone_Lan`, `Zone_Office`, `Zone_Subnet`

## Deployment Nodes

`Node_Environment`, `Node_Datacenter`, `Node_Cicd`, `Node_Cluster`, `Node_Vm`, `Node_Server`, `Node_App`, `Node_AppBrowser`, `Node_AppMobile`, `Node_AppRich`, `Node_External`, `Node_SaaS`, `Node_Container`

## Infrastructure

`Infra_F5`, `Infra_Fw`, `Infra_Router`

## Relationship Kinds (Model)

`calls`, `async`, `reads`, `writes`, `uses`

## Relationship Kinds (Deployment)

`http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`

## Usage Example

```likec4
// Element kinds: PascalCase, underscore-separated category_subtype
api = Container_Api 'REST API' {
  technology 'Node.js'
  description 'Public API surface'
}

// Relationship kinds: in arrow, never in property block
api -[calls]-> external 'Authenticate'
api -[reads]-> database 'Fetch records'
api -[async]-> queue 'Publish job'
```

## Common Mistakes

❌ **Guessing names from English labels** — `Container_API`, `Infra_Firewall`, `Node_VM` are invalid in this repository.

❌ **Defaulting to a generic base kind** — `Container` exists, but for common application elements prefer a specific declared subtype like `Container_Api` or `Container_Database`.

❌ **Inventing relationship kinds** — only use the declared relationship kinds; `invokes`, `triggers` are invalid

❌ **Confusing model and deployment kinds** — `http`/`https`/`tcp` are deployment relationship kinds; `calls`/`async` are model kinds
