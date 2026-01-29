# ADR-0004: MVP Plugin Selection

## Status

Accepted

## Context

Forgejo offers extensive functionality through built-in features and optional plugins. Dev-Forge's initial deployment must prioritize essential capabilities while avoiding feature bloat that increases complexity and maintenance burden.

**Principles**:
- **Minimum Viable Product (MVP)**: Deploy only features necessary for core workflows
- **Iterative Release**: Add features based on actual usage patterns, not speculation
- **Operational Simplicity**: Each feature adds configuration complexity and potential failure modes
- **Team Capacity**: Limited resources for initial deployment and support

**Core Development Workflow** (must support):
1. Developer authentication (corporate identity integration)
2. Create/clone Git repositories
3. Push code, trigger CI/CD automatically
4. Pull dependencies from package registry
5. Request code review via merge requests
6. Merge approved changes to main branch

**Deferred for Future Phases**:
- Issue tracking and project management (existing Jira integration)
- Wiki and documentation (existing Confluence)
- Advanced security scanning (can add later)
- Container registry native features (using Nexus integration)

### Plugin Evaluation Matrix

| Plugin/Feature | Essential? | Complexity | Maturity | Decision |
|----------------|-----------|------------|----------|----------|
| **Authentication (LDAP/OIDC)** | ✅ Yes | Low | High | **MVP** |
| **Actions (CI/CD)** | ✅ Yes | Medium | High | **MVP** |
| **Repositories** | ✅ Yes | Low | High | **MVP** |
| **Registry (Nexus bridge)** | ✅ Yes | Medium | Medium | **MVP** |
| **Code Review (MR)** | ✅ Yes | Low | High | **MVP** |
| **Pages (Static hosting)** | ✅ Yes | Low | High | **MVP** |
| Issue Tracking | ❌ No | Low | High | Phase 2 |
| Project Boards | ❌ No | Low | Medium | Phase 2 |
| Wiki | ❌ No | Low | High | Phase 2 |
| Packages (native) | ❌ No | High | Medium | Deferred |
| LFS (Git Large Files) | ⚠️ Maybe | Low | High | Phase 2 |
| GPG Commit Signing | ⚠️ Maybe | Low | High | Phase 2 |
| Webhooks | ⚠️ Maybe | Low | High | Included by default |
| External Auth (GitHub OAuth) | ❌ No | Low | Medium | Not needed |

## Decision

Dev-Forge MVP will include **exactly six essential plugins**:

### 1. Authentication Plugin (LDAP/OIDC)
**Rationale**: Corporate identity integration is non-negotiable for enterprise deployment.

**Features**:
- LDAP integration with Active Directory
- OIDC integration with SSO provider (Keycloak, etc.)
- Group-based admin privilege mapping
- Automatic user provisioning on first login

**Why Essential**: Cannot rely on local accounts—must integrate with organizational identity management.

**Complexity**: Low (well-documented, stable)

### 2. Actions Plugin (CI/CD)
**Rationale**: Automated testing and building is core to modern development workflow.

**Features**:
- GitHub Actions-compatible syntax
- Containerized workflow execution
- Secrets management
- Manual and automated triggers
- Status checks for merge requests

**Why Essential**: Continuous integration is fundamental/expected for any Git platform. Without CI/CD, Dev-Forge is just a Git host.

**Complexity**: Medium (runner management, auto-scaling)

### 3. Repositories Plugin (Git Hosting)
**Rationale**: Core Git functionality is the foundation of the platform.

**Features**:
- Git clone/push/pull (HTTPS and SSH)
- Branch and tag management
- Branch protection rules
- Access control (public/internal/private)
- File browser and history

**Why Essential**: This is the primary function—everything else builds on Git hosting.

**Complexity**: Low (built-in, mature)

### 4. Registry Plugin (Nexus Integration)
**Rationale**: Developers need centralized dependency management.

**Features**:
- Proxy/bridge to existing Nexus instance
- npm, Maven, Docker, PyPI, NuGet support
- Unified authentication (Forgejo credentials → Nexus tokens)
- Integrated UI for package browsing

**Why Essential**: Modern development requires package/dependency management. Using existing Nexus avoids duplicate infrastructure while providing seamless developer experience.

**Complexity**: Medium (integration configuration, authentication bridge)

### 5. Code Review Plugin (Merge Requests)
**Rationale**: Collaborative code review is critical for code quality and knowledge sharing.

**Features**:
- Merge request workflow (pull requests)
- Inline code comments and discussions
- Approval requirements and gatekeeping
- Integration with Actions (status checks)
- Auto-merge capability

**Why Essential**: Code review is best practice for any professional development team. Enables collaboration and maintains quality standards.

**Complexity**: Low (built-in, well-developed)

### 6. Pages Plugin (Static Site Hosting)
**Rationale**: Documentation and project sites are common needs for development teams, enabling self-service static website hosting from repositories.

**Features**:
- Host static websites directly from repository branches (e.g., `gh-pages`, `main/docs/`)
- Automatic deployment on push
- Custom domain support (via CNAME)
- HTTPS encryption
- Similar to GitHub Pages experience

**Why Essential**: Teams frequently need to host project documentation, API references, demos, and landing pages. Integrated hosting eliminates need for separate web hosting infrastructure and provides streamlined workflow (commit → publish).

**Complexity**: Low (built-in Forgejo feature, minimal configuration)

## Consequences

### Positive Consequences

- **Focused Deployment**: Clear scope limits initial complexity
- **Faster Time-to-Value**: Developers can start using platform immediately for core workflows
- **Lower Risk**: Fewer moving parts means fewer potential failure points
- **Clear Success Criteria**: MVP defines what "working" means
- **Iterative Improvement**: Can add features based on actual demand
- **Operational Simplicity**: Support team has manageable surface area
- **Training Focus**: Onboarding documentation covers essentials only

### Negative Consequences

- **Limited Feature Set**: Some developers may expect features not in MVP (issue tracking, wikis)
- **Integration Gaps**: Must use external tools (Jira) for some workflows
- **Perception Risk**: "Missing features" may create impression of incomplete platform
- **Future Complexity**: Adding plugins later requires migration/update planning
- **Workaround Development**: Teams may build custom solutions for missing features

### Neutral Consequences

- **Integration Required**: Nexus bridge needs testing and validation
- **Documentation Scope**: Only document MVP features (simplifies docs)
- **Support Burden**: Support team specialists on six features (vs entire platform)

## Notes

### Phase 2 Candidates

Based on MVP feedback, next plugins to consider:

**High Priority**:
- Git LFS (if teams work with large binary files)
- Issue tracking (if Jira integration proves insufficient)
- GPG commit signing (if security policy requires)

**Medium Priority**:
- Project boards/kanban
- Wiki (if lightweight docs needed)
- Advanced webhooks (integrations)

**Low Priority**:
- External authentication providers (GitHub OAuth)
- Native package registry (if Nexus becomes limiting)
- Advanced security scanning (SAST/DAST)

### Success Metrics

MVP is successful if, after 90 days:
- 80%+ developers actively use platform for code hosting
- 60%+ projects have CI/CD workflows configured
- 40%+ merge requests use code review workflow
- < 5% support tickets about missing features
- Zero P1/P2 incidents related to core plugins

### Plugin Implementation Details

See [Reference: MVP Plugins](../docs/reference/plugins-mvp.md) for detailed configuration and usage.

### Related Decisions

- [ADR-0001: Forgejo Platform](0001-forgejo-platform.md) — Platform provides plugin infrastructure
- [ADR-0002: Actions Scalability](0002-actions-scalability.md) — Actions plugin scalability strategy
- [ADR-0007: Nexus Integration](0007-nexus-integration.md) — Registry plugin architecture

### References

- Forgejo Features Overview: https://forgejo.org/docs/latest/user/
- MVP Product Development: https://en.wikipedia.org/wiki/Minimum_viable_product
- Internal feature request tracking (Confluence: "Dev-Forge Feature Requests")
