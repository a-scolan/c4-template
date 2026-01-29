# Dev-Forge: Modern Development Platform

**An on-premises, technology-agnostic development platform powered by Forgejo and Puppet**

Dev-Forge provides development teams with a complete, self-hosted Git platform featuring CI/CD automation, code review, package management, and automated infrastructure provisioning—all whilst remaining neutral to the programming languages and frameworks teams choose to use.

## 🎯 Project Overview

**Status**: Initial Planning & Documentation Phase  
**Target Environment**: On-premises infrastructure  
**Initial Deployment**: Staging environment with scalable Forgejo Actions runners  
**Future**: Production environment following validated staging architecture

### Core Technologies

- **Forgejo**: Git hosting, CI/CD (Actions), code review, package registry integration
- **Puppet**: Infrastructure automation and configuration management
- **Nexus**: External package registry (existing integration)
- **PostgreSQL**: Forgejo database backend

## 📚 Documentation Structure (Diataxis Framework)

This project follows the [Diataxis](https://diataxis.fr/) documentation framework, organizing content by user needs:

### 📖 [Tutorials](projects/dev-forge/docs/tutorial/) — Learning by Doing
*For developers new to the platform*

- [01 - Onboarding Developer](projects/dev-forge/docs/tutorial/01-onboarding-developer.md) — Create your first repository
- [02 - First Pipeline](projects/dev-forge/docs/tutorial/02-first-pipeline.md) — Set up CI/CD with Forgejo Actions

### 🔧 [How-To Guides](projects/dev-forge/docs/how-to/) — Practical Tasks
*For working practitioners accomplishing specific goals*

- [Configure Runners](projects/dev-forge/docs/how-to/configure-runners.md) — Scale and configure Forgejo Actions runners
- [Setup Plugins](projects/dev-forge/docs/how-to/setup-plugins.md) — Activate and configure MVP plugins
- [Puppet Tasks](projects/dev-forge/docs/how-to/puppet-tasks.md) — Expected outcomes for deployment tasks

### 📋 [Reference](projects/dev-forge/docs/reference/) — Technical Facts
*For practitioners needing specifications and details*

- [MVP Plugins](projects/dev-forge/docs/reference/plugins-mvp.md) — Auth, Actions, Repos, Registry, Code Review
- [Forgejo Configuration](projects/dev-forge/docs/reference/forgejo-config.md) — System configuration reference

### 💡 [Explanation](projects/dev-forge/ADR/) — Understanding Decisions
*For understanding the "why" behind architectural choices*

See [Architecture Decision Records (ADRs)](projects/dev-forge/ADR/) for detailed rationale:
- ADR-0001: Forgejo Platform Selection
- ADR-0002: Actions Scalability Strategy
- ADR-0003: Puppet Automation
- ADR-0004: MVP Plugins Selection
- ADR-0005: Network Zone Architecture
- ADR-0006: Technology Neutrality
- ADR-0007: Nexus Registry Integration

## 🏗️ Architecture & Models

### C4 Architecture Models (LikeC4)

Comprehensive system architecture modelled at all C4 levels:

- **[System Model](projects/dev-forge/system-model.c4)** — Elements, containers, and components
- **[System Views](projects/dev-forge/system-views.c4)** — Context, container, and component diagrams
- **[Deployment (Staging)](projects/dev-forge/deployment-staging.c4)** — Infrastructure topology and runtime environment

**Preview Models**: Use the LikeC4 MCP server or VS Code extension to visualize diagrams

### Workflow Diagrams (Mermaid)

*Coming in Phase 6*: Visual workflows for common tasks
- Developer onboarding flow
- CI/CD trigger and execution
- Runner auto-scaling behaviour
- Puppet deployment orchestration

## 🚀 Project Progress

See [PROJECT_CHECKLIST.md](projects/dev-forge/PROJECT_CHECKLIST.md) for detailed phase tracking:

- ✅ **Phase 1**: Documentation Structure (Diataxis)
- ✅ **Phase 2**: Architecture Decision Records
- 🔄 **Phase 3**: C4 Architecture Modelling
- ⏳ **Phase 4**: Model Validation & Preview
- ⏳ **Phase 5**: Production Environment Extension
- ⏳ **Phase 6**: Workflow Diagrams (Mermaid)

## 💎 Key Principles

1. **Technology Agnostic**: Platform supports any programming language or framework
2. **Scalable CI/CD**: Containerized Forgejo Actions runners with auto-scaling
3. **On-Premises First**: Complete control over infrastructure and data
4. **Automated Operations**: Puppet-driven provisioning and configuration
5. **Modular Design**: MVP plugin approach ensures focused, maintainable platform

## 🤝 Contributing

Architecture questions? Start with [ADRs](projects/dev-forge/ADR/)  
Implementation questions? Check [How-To Guides](projects/dev-forge/docs/how-to/)  
Need to understand something? Read [Explanations](projects/dev-forge/ADR/)  
Ready to learn? Follow [Tutorials](projects/dev-forge/docs/tutorial/)

---

**Note**: This is a living architecture. As the platform evolves, documentation and models will be updated to reflect current design decisions and implementation details
| `.github/copilot-instructions.md` | Copilot workflow guidance | How Copilot should work in your project |
| `.github/skills/` | 14 skill files | Architecture helpers for Copilot |
| `projects/shared/spec-*.c4` | 6 specification files | Reusable element kinds, tags, relationships |
| `projects/shared/images/` | 28+ SVG icons | Shared architecture diagrams |
| `projects/spec-showcase/` | Example C4 diagrams | Reference examples |

**Important:** Always update all three directories together so your project stays in sync with the template's specification standards.

**Note:** The `--squash` flag (git subtree only) consolidates all c4-template changes into one commit per sync. Updates are manual—they do not happen automatically.

#### When to Sync

- **Quarterly:** Regular maintenance to stay current
- **When template skills improve:** Better Copilot assistance
- **When specs are updated:** Align with latest conventions
- **When new icons added:** More diagram options

---

## Project-Specific READMEs

This README documents the template. When creating a **project-specific repository** (e.g., for a domain like NiceLabel, banking, healthcare), create a project-specific README that:

1. Documents your architecture and systems
2. Describes how you've configured template synchronization
3. Lists which Copilot skills apply to your domain
4. Includes project-specific best practices
5. Documents your ADRs and key architectural decisions

