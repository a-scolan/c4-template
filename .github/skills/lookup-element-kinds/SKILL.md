---
name: lookup-element-kinds
description: Use when creating elements or relationships and you need to validate kind names, discover available types, or check specification consistency.
---

# LikeC4 Element Kinds and Relationship Types Reference

Use this skill when you need to check available element kinds and relationship types.

**Keywords:** Actor, System, Container, Component, Zone, Node, Infrastructure, relationship kinds, type validation, specification

**Always confirm with MCP:** Use `read-project-summary` to validate the current shared spec in the active workspace. This list is a quick reference and may evolve.

## Actors (C1)

`Actor_Person`, `Actor_Staff`, `Actor_Admin`

## Systems (C1)

`System_Existing`, `System_New`, `System_Legacy`, `System_External`

## Containers (C2)

`Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_Cache`, `Container_WebServer`, `Container_Loadbalancer`, `Container_ObjectStorage`, `Container_FileServer`, `Container_ProcessingServer`, `Container_Mailserver`, `Container_IamServer`, `Container_ExchangeServer`, `Container_ApplicationServer`, `Container_Spa`, `Container_MobileApp`, `Container_Browser`, `Container_ReverseProxy`, `Container_Waf`, `Container_Firewall`, `Container_DataServer`, `Container_Directory`, `Container_Api_Geo`, `Container_DatabaseGeo`

## Components (C3)

`Component`

## Deployment Zones

`Zone`, `Zone_Internet`, `Zone_Vlan`, `Zone_Lan`

## Deployment Nodes

`Node_Environment`, `Node_Vm`, `Node_Server`, `Node_App`, `Node_Container`, `Node_Pod`, `Node_Cluster`

## Infrastructure

`Infra_F5`, `Infra_Firewall`, `Infra_Router`, `Infra_Switch`, `Infra_Vpn`

## Relationship Kinds (Model)

`calls`, `async`, `reads`, `writes`, `uses`

## Relationship Kinds (Deployment)

`http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`, `smtp`, `ldap`, `oidc_saml`
