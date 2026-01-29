# ADR-0007: Nexus Registry Integration

## Status

Accepted

## Context

Modern development requires centralized package/dependency management across multiple ecosystems (npm, Maven, PyPI, Docker, NuGet). Dev-Forge needs a package registry solution that is:

**Requirements**:
- Multi-ecosystem support (at least npm, Maven, Docker)
- On-premises deployment (organizational requirement)
- Technology-neutral (supports all major package managers)
- Scalable and performant
- Well-integrated with source control workflow

**Organizational Context**:
- **Nexus Repository Manager is already deployed** and in production use
- Infrastructure team maintains Nexus for dependency management
- Developers familiar with Nexus URLs and workflows
- Existing Nexus configuration (repositories, proxies, security)
- Investment in Nexus infrastructure and expertise

**Forgejo Capabilities**:
- Forgejo includes **native package registry** (experimental/newer feature)
- Supports npm, Maven, Docker, PyPI, NuGet, and more
- Integrated authentication (Forgejo users/tokens)
- Unified UI (packages appear alongside code)

### Alternatives Considered

**Forgejo Native Registry**:
- ✅ Seamless integration with repositories and CI/CD
- ✅ Single authentication system (Forgejo credentials)
- ✅ Unified UI (code + packages in one place)
- ✅ Simplified architecture (one less service)
- ❌ **Duplicate infrastructure** (Nexus already exists)
- ❌ **Immature feature** (newer, less battle-tested)
- ❌ **Migration burden** (move existing artifacts to Forgejo)
- ❌ **Lost expertise** (team knows Nexus, not Forgejo registry)
- ❌ **Operational overhead** (another system to back up, monitor, scale)

**JFrog Artifactory**:
- ✅ Feature-rich, enterprise-grade
- ✅ Excellent multi-ecosystem support
- ✅ Advanced features (build info, artifact promotion)
- ❌ **Expensive licensing** (commercial product)
- ❌ **Nexus already deployed** (sunk cost, established workflows)
- ❌ **Migration required** from Nexus

**Self-Hosted Ecosystem Registries** (npm registry, PyPI server, Docker registry separately):
- ✅ Lightweight, purpose-built
- ✅ Well-documented for each ecosystem
- ❌ **Operational complexity** (manage many services)
- ❌ **Inconsistent experience** (different auth, UI, processes per ecosystem)
- ❌ **Nexus already provides this** (consolidation via Nexus)

**Cloud Package Registries** (npm, Docker Hub, PyPI.org directly):
- ✅ Zero infrastructure management
- ✅ High availability and performance
- ❌ **Violates on-premises requirement**
- ❌ **Dependency on external services**
- ❌ **Data sovereignty concerns** (cannot cache closed-source packages internally)
- ❌ **Outbound internet dependency**

## Decision

Dev-Forge will **integrate with existing Nexus Repository Manager** via a proxy/bridge pattern, rather than using Forgejo's native package registry.

### Architecture

**Nexus as Source of Truth**:
- All packages stored in Nexus repositories
- Nexus manages proxying to public registries (npm, Maven Central, Docker Hub)
- Nexus enforces storage quotas and retention policies

**Forgejo as Unified Gateway**:
- Forgejo provides unified endpoint: `https://forge.company.internal/api/packages/{ecosystem}/`
- Forgejo authenticates users via Forgejo credentials
- Forgejo generates temporary Nexus user tokens
- Requests proxied to Nexus with token authentication
- Responses returned to client transparently

**Benefits**:
- Developers use Forgejo credentials (no separate Nexus login)
- CI/CD workflows use Forgejo tokens (consistent auth)
- Packages accessible via Git platform URL (logical grouping)
- Nexus remains source of truth (existing workflows unchanged)

### Integration Pattern

```
Developer/CI
    ↓
    Forgejo Package API
    (https://forge.company.internal/api/packages/npm/)
    ↓
    [Authentication: Forgejo credentials]
    ↓
    [Token Exchange: Generate Nexus token]
    ↓
    Nexus Repository
    (https://nexus.company.internal/repository/npm-group/)
    ↓
    [Proxy to public registries if needed]
    ↓
    Return package to client
```

**Session Flow**:
1. Client authenticates to Forgejo (`npm login`)
2. Forgejo validates Forgejo credentials
3. Forgejo calls Nexus API: "Generate user token for user@company.com"
4. Nexus returns temporary token (TTL: 1 hour)
5. Forgejo caches token (Redis/memory)
6. Subsequent requests use cached token until expiration
7. Token renewed automatically on expiration

### Configuration

**Forgejo `app.ini`**:
```ini
[packages]
ENABLED = true

[packages.proxy]
TYPE = nexus
URL = https://nexus.company.internal
TIMEOUT = 30s

[packages.auth]
NEXUS_TOKEN_URL = https://nexus.company.internal/service/rest/v1/security/user-tokens
FORWARD_CREDENTIALS = true
TOKEN_CACHE_TTL = 3600

[packages.npm]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/npm-group/

[packages.maven]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/maven-public/

[packages.docker]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/docker-hosted/
```

**Nexus Configuration**:
- Forgejo service account with token generation permission
- LDAP/OIDC integration (same identity provider as Forgejo)
- API access enabled for user token creation

## Consequences

### Positive Consequences

- **No Duplicate Infrastructure**: Reuses existing Nexus investment
- **Proven Stability**: Nexus is mature, battle-tested for package management
- **Unified Developer Experience**: Single Forgejo login for code + packages
- **Consistent CI/CD**: Same authentication token for Git and packages
- **Existing Workflows Preserved**: Nexus users can continue direct access
- **Expertise Leveraged**: Infrastructure team's Nexus knowledge applies
- **Centralized Storage**: All packages in one system (Nexus)—simplifies backups
- **Gradual Migration**: Can evaluate Forgejo native registry later without urgency

### Negative Consequences

- **Integration Complexity**: Proxy/bridge adds architectural layer
- **Authentication Latency**: Token exchange adds ~100-200ms per initial request
- **Dependency on Nexus**: Nexus downtime affects Dev-Forge package access
- **Limited Forgejo UI**: Packages not browsable in Forgejo web interface (must use Nexus UI)
- **Two Configuration Points**: Changes require updates in both Forgejo and Nexus
- **Token Management**: Must monitor token generation rate and cache effectiveness

### Neutral Consequences

- **Native Registry Deferred**: Can revisit decision if Forgejo registry matures significantly
- **Nexus Monitoring**: Must ensure Nexus scaled appropriately for increased load
- **Fallback Option**: Direct Nexus URLs remain available as fallback

## Notes

### Nexus Repository Structure

**Recommended Setup**:
- **Hosted repositories**: Internal packages (published by developers)
- **Proxy repositories**: Cache public registries (npm, Maven Central)
- **Group repositories**: Combine hosted + proxy (single endpoint)

**Example**:
- `npm-hosted`: Internal company npm packages
- `npm-proxy`: Cache npmjs.org
- `npm-group`: Combines hosted + proxy → Forgejo points here

### Migration Path to Native Registry (Future)

If Forgejo native registry becomes compelling:

1. **Evaluation Phase**: Test Forgejo registry in staging with subset of packages
2. **Dual Operation**: Run both Nexus and Forgejo registry (gradual migration)
3. **Migration**: Sync packages from Nexus to Forgejo
4. **Cutover**: Update CI/CD to use native Forgejo endpoints
5. **Decommission**: Phase out Nexus dependency

**Decision Criteria for Migration**:
- Forgejo registry feature parity with Nexus (maturity)
- Migration tooling availability
- No operational disruption
- Clear benefits over integration (performance, features, cost)

### Security Considerations

**Token Security**:
- Tokens cached in memory/Redis (not persisted to disk)
- Tokens auto-expire (1 hour TTL)
- Forgejo logs token generation for audit

**Network Security**:
- Forgejo ↔ Nexus communication over HTTPS
- Nexus not directly Internet-accessible (behind firewall)
- Nexus API authentication via service account (least privilege)

### Performance Optimization

**Caching Strategy**:
- Token caching reduces Nexus API calls (improves latency)
- Forgejo does NOT cache package data (Nexus handles this)
- HTTP caching headers passed through transparently

**Monitoring Metrics**:
- Token cache hit rate (target: > 90%)
- Token exchange latency (target: < 200ms p95)
- Nexus request rate from Forgejo
- Package download throughput

### Related Decisions

- [ADR-0004: MVP Plugins](0004-mvp-plugins.md) — Registry plugin as part of MVP
- [ADR-0006: Technology Neutrality](0006-tech-neutrality.md) — Nexus supports all ecosystems
- [ADR-0001: Forgejo Platform](0001-forgejo-platform.md) — Forgejo as primary developer interface

### References

- Nexus Repository Manager Documentation: https://help.sonatype.com/repomanager3
- Nexus REST API: https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api
- Nexus User Token API: https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api/user-account-api
- Internal Nexus documentation (Confluence: "Infrastructure/Nexus")
