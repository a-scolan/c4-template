# ADR-0006: Technology Neutrality Principle

## Status

Accepted

## Context

Dev-Forge serves development teams working with diverse programming languages, frameworks, and toolchains. The platform must not impose technical constraints or favor specific ecosystems.

**Team Diversity**:
- Backend: Java (Spring Boot), Python (Django, Flask), Go, Node.js
- Frontend: React, Vue.js, Angular, vanilla JavaScript
- Mobile: Swift, Kotlin, React Native
- Infrastructure: Terraform, Ansible, shell scripts
- Data: Python (pandas, scikit-learn), R, SQL

**Historical Challenges**:
- Previous internal tools favored specific languages (Java-centric CI/CD)
- Developers avoided platform due to poor support for their stack
- Custom workarounds created maintenance burden
- Teams built shadow IT solutions outside official platform

**Requirements**:
- Support any language/framework without special configuration
- No baked-in assumptions about build tools or package managers
- Enable polyglot projects (multiple languages in one repository)
- Allow teams to adopt new technologies without platform changes

### Alternatives Considered

**Language-Specific Optimizations**:
- ✅ Best-in-class experience for supported languages
- ✅ Built-in templates and patterns
- ❌ **Excludes teams using other stacks**
- ❌ Requires platform updates for new language adoption
- ❌ Creates second-class citizen stigma for unsupported languages

**Restricted Technology List**:
- ✅ Simplifies support and troubleshooting
- ✅ Standardization reduces complexity
- ❌ **Stifles innovation and experimentation**
- ❌ Forces technology choices on teams
- ❌ Platform becomes bottleneck for new tools

**Per-Language Services**:
- ✅ Specialized services for each ecosystem
- ✅ Deep integration (Maven repository, npm registry separate)
- ❌ High operational complexity (many services to maintain)
- ❌ Inconsistent user experience across languages
- ❌ Scales poorly as technology landscape evolves

**Containerization Only**:
- ✅ Maximum flexibility (bring your own container)
- ✅ Language-agnostic by design
- ❌ Steep learning curve (requires Docker expertise)
- ❌ Overhead for simple projects
- ❌ Does not solve package registry integration

## Decision

Dev-Forge will adhere to a **strict technology neutrality principle**:

### Core Principles

**1. No Language Assumptions**
- Platform makes zero assumptions about project language or framework
- No special configuration required for any language
- No "blessed" or "preferred" technologies promoted

**2. Generic Infrastructure**
- CI/CD runners provide generic Linux environments (Ubuntu LTS)
- Workflows specify their dependencies explicitly (not pre-installed)
- Package registries support all major ecosystems equally

**3. Bring Your Own Toolchain**
- Projects define their build/test/deploy tools in workflow files
- No platform-imposed build systems or conventions
- Teams choose tools based on requirements, not platform limitations

**4. Polyglot Support**
- Single repository can contain multiple languages
- CI/CD workflows handle mixed technology stacks
- No artificial boundaries between ecosystems

### Implementation

#### CI/CD (Forgejo Actions)

**Generic Runner Image**: `ubuntu-latest`
```yaml
# Example: Node.js project
- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'

# Example: Python project  
- name: Setup Python
  uses: actions/setup-python@v3
  with:
    python-version: '3.11'

# Example: Java project
- name: Setup Java
  uses: actions/setup-java@v3
  with:
    java-version: '17'
    distribution: 'temurin'
```

**Key Pattern**: Workflows explicitly declare dependencies—platform provides primitiveness, projects provide specificity.

#### Package Registry (Nexus Integration)

**Ecosystem Support**:
- npm (JavaScript/TypeScript)
- Maven (Java)
- PyPI (Python)
- NuGet (.NET)
- Docker (containers)
- (Future: RubyGems, Cargo, Go modules)

**Uniform Access**: `https://forge.company.internal/api/packages/{ecosystem}/`

**Authentication**: Same credentials regardless of ecosystem

**No Preference**: All ecosystems equally supported, no "primary" language

#### Repository Management

**No Language Detection**:
- Platform does not analyze code to determine language
- No automatic badge generation based on project type
- No language-specific features in repository browser

**File Format Agnostic**:
- Syntax highlighting for all languages (via universal library)
- No assumptions about build files (package.json, pom.xml, etc.)

#### Documentation & Examples

**Language-Neutral Docs**:
- Tutorials show workflows for multiple languages (Node.js, Python, Go examples)
- How-to guides avoid language-specific advice
- Reference documentation covers configurability, not conventions

**Community Contributions**:
- Template repositories for common stacks (community-driven)
- Not official platform recommendations—just examples

## Consequences

### Positive Consequences

- **Universal Adoption**: Any team can use platform regardless of tech stack
- **Future-Proof**: New languages/frameworks supported without platform changes
- **Innovation-Friendly**: Teams can experiment with emerging technologies
- **No Vendor Lock-In**: Platform does not dictate technology choices
- **Consistent Experience**: Same workflows/patterns apply to all languages
- **Reduced Bias**: Eliminates perception of favoritism towards specific ecosystems
- **Simplified Operations**: One runtime environment (Linux) supports everything

### Negative Consequences

- **No Optimization**: Cannot deeply optimize for specific language quirks
- **Learning Curve**: Teams must configure their own toolchain (not pre-configured)
- **Template Proliferation**: Need many examples to cover all languages
- **Support Complexity**: Support team must understand diverse ecosystems
- **Troubleshooting**: Harder to diagnose language-specific issues
- **Resource Usage**: Some workflows inefficient due to runtime installation overhead

### Neutral Consequences

- **Community Responsibility**: Teams contribute examples for their stacks
- **Documentation Burden**: More examples needed to cover common cases
- **Performance Variability**: Workflow speed depends on toolchain download time

## Notes

### Acceptable Exceptions

Neutrality is not absolutism. Acceptable concessions:

**Security Scanning**:
- May support language-specific scanners (e.g., npm audit, Snyk)
- Always optional, never required

**Default Worker Images**:
- Ubuntu LTS chosen for broad compatibility
- Does not preclude custom Docker images

**Package Registry**:
- Support ecosystems as they gain mainstream adoption
- Prioritize based on organizational usage, not personal preference

### Language Adoption Process

When teams want a new language/framework:

1. **No Permission Required**: Teams can use any language immediately
2. **CI/CD Workflow**: Team writes `setup-<language>` steps
3. **Package Registry**: If needed, request Nexus repository (standard process)
4. **Share Examples**: Optionally contribute template to help others

### Monitoring Language Diversity

Track (but do not restrict) language usage to understand platform effectiveness:
- Count projects by primary language (via `.gitattributes` or repository metadata)
- Monitor CI/CD workflow diversity
- Identify underserved ecosystems for potential registry additions

### Polyglot Project Example

```yaml
# Monorepo with backend (Go), frontend (React), and infra (Terraform)
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v3
        with:
          go-version: '1.21'
      - run: cd backend && go test ./...
  
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci && npm test
  
  infrastructure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: '1.6'
      - run: cd infra && terraform validate
```

### Related Decisions

- [ADR-0002: Actions Scalability](0002-actions-scalability.md) — Generic runner architecture enables neutrality
- [ADR-0004: MVP Plugins](0004-mvp-plugins.md) — Package registry supports multiple ecosystems
- [ADR-0007: Nexus Integration](0007-nexus-integration.md) — Nexus chosen for multi-ecosystem support

### References

- GitHub Actions Environments: https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners
- Polyglot Programming: https://en.wikipedia.org/wiki/Polyglot_(computing)
- Internal technology survey (Confluence: "Tech Stack Inventory")
