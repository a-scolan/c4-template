# Référence : Plugins MVP

Référence technique pour l'ensemble de plugins minimum viable product (MVP) de Dev-Forge.

---

## Vue d'Ensemble des Plugins

| Plugin | Objectif | Statut Implémentation |
|--------|---------|----------------------|
| Authentication | Intégration LDAP/OIDC | ✅ Documenté |
| Actions | Automatisation CI/CD | ✅ Documenté |
| Repositories | Hébergement Git | ✅ Documenté |
| Registry | Gestion packages | ✅ Documenté |
| Code Review | Workflows merge request | ✅ Documenté |
| Pages | Hébergement site statique | ✅ Documenté |

---

## 1. Plugin Authentication

### Backends Supportés

#### LDAP/Active Directory

**Section de Configuration** : `[auth.ldap.*]`

**Paramètres Requis** :
- `HOST` : Nom d'hôte ou IP serveur LDAP
- `PORT` : Port serveur LDAP (389 non chiffré, 636 pour LDAPS)
- `SECURITY_PROTOCOL` : `unencrypted` | `ldaps` | `starttls`
- `BIND_DN` : Distinguished name compte service
- `BIND_PASSWORD` : Mot de passe compte service
- `USER_BASE` : DN de base pour recherches utilisateur
- `USER_FILTER` : Filtre LDAP pour lookup utilisateur (utiliser `%s` comme placeholder nom d'utilisateur)

**Paramètres Optionnels** :
- `ADMIN_FILTER` : Filtre LDAP pour identifier utilisateurs administrateur
- `USERNAME_ATTRIBUTE` : Attribut contenant nom d'utilisateur (défaut : `uid`)
- `EMAIL_ATTRIBUTE` : Attribut contenant email (défaut : `mail`)
- `FIRST_NAME_ATTRIBUTE` : Attribut pour prénom (défaut : `givenName`)
- `SURNAME_ATTRIBUTE` : Attribut pour nom (défaut : `sn`)

**Exemple** :
```ini
[auth.ldap.corporate]
NAME = Corporate LDAP
ENABLED = true
HOST = ldap.company.internal
PORT = 389
SECURITY_PROTOCOL = unencrypted
BIND_DN = cn=forgejo,ou=services,dc=company,dc=internal
BIND_PASSWORD = SecurePassword123
USER_BASE = ou=users,dc=company,dc=internal
USER_FILTER = (uid=%s)
ADMIN_FILTER = (memberOf=cn=devforge-admins,ou=groups,dc=company,dc=internal)
USERNAME_ATTRIBUTE = uid
EMAIL_ATTRIBUTE = mail
```

#### OpenID Connect (OIDC)

**Configuration Section**: `[oauth2.*]`

**Required Parameters**:
- `NAME`: Display name for authentication provider
- `ENABLED`: `true` to activate
- `CLIENT_ID`: OAuth2 client identifier
- `CLIENT_SECRET`: OAuth2 client secret
- `OPENID_CONNECT_AUTO_DISCOVERY_URL`: OIDC discovery endpoint URL

**Optional Parameters**:
- `SCOPES`: Space-separated list of OAuth2 scopes (default: `openid profile email`)
- `ENABLE_AUTO_REGISTRATION`: Automatically create accounts on first login

**Example**:
```ini
[oauth2_client]
ENABLE_AUTO_REGISTRATION = true

[oauth2.keycloak]
NAME = Corporate SSO
ENABLED = true
CLIENT_ID = forgejo-staging
CLIENT_SECRET = a1b2c3d4-e5f6-7890-abcd-ef1234567890
OPENID_CONNECT_AUTO_DISCOVERY_URL = https://sso.company.internal/auth/realms/company/.well-known/openid-configuration
SCOPES = openid profile email groups
```

### Account Synchronization

**Behavior**:
- **First login**: User account created automatically
- **Subsequent logins**: Profile attributes updated from identity provider
- **Deprovisioning**: Manual account disable required (or via API)

**Admin Privilege Mapping**:
- **LDAP**: Via `ADMIN_FILTER` (group membership)
- **OIDC**: Via groups claim in ID token (requires configuration)

### Implementation Notes

**TODO**: Document actual LDAP server addresses and group DNs after staging deployment.

**TODO**: Obtain OIDC client credentials from SSO administrator.

**TODO**: Test account lifecycle (creation, update, deletion) in staging environment.

---

## 2. Plugin Actions (CI/CD)

### Core Configuration

**Configuration Section**: `[actions]`

**Required Parameters**:
- `ENABLED`: `true` to activate Actions
- `DEFAULT_ACTIONS_URL`: URL for public Actions/workflows repository (default: `https://code.forgejo.org`)

**Example**:
```ini
[actions]
ENABLED = true
DEFAULT_ACTIONS_URL = https://code.forgejo.org
```

### Runner Configuration

**Runner Types**:
- `ubuntu-latest`: Default Linux runner (Ubuntu 22.04)
- `docker`: Runner with Docker-in-Docker capability
- High-memory runners: Custom label for resource-intensive jobs

**Registration**:
```bash
# Generate registration token in Forgejo admin panel
# Then register runner with:
forgejo-runner register \
  --instance https://forge.company.internal \
  --token <REGISTRATION_TOKEN> \
  --labels ubuntu-latest,docker
```

**Runner Resource Defaults**:
| Resource | Default | High-Memory | Notes |
|----------|---------|-------------|-------|
| CPU | 2 vCPU | 4 vCPU | Adjustable per runner type |
| Memory | 4 GB | 8 GB | Container memory limit |
| Disk | 20 GB | 50 GB | Ephemeral storage |
| Timeout | 60 min | 120 min | Default job timeout |

### Workflow Syntax

**Minimal Workflow**:
```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run build
        run: make build
```

**Supported Triggers**:
- `push`: Code pushed to repository
- `pull_request`: Merge request opened/updated
- `schedule`: Cron-based scheduling
- `workflow_dispatch`: Manual trigger
- `repository_dispatch`: Webhook trigger

**Runner Label Selection**:
```yaml
jobs:
  heavy-build:
    runs-on: high-memory
    steps:
      - name: Build large application
        run: ./build-heavy.sh
```

### Available Actions

**Official Actions** (from Forgejo):
- `actions/checkout@v3`: Clone repository
- `actions/setup-node@v3`: Set up Node.js
- `actions/setup-python@v3`: Set up Python
- `actions/cache@v3`: Cache dependencies
- `actions/upload-artifact@v3`: Upload build artifacts
- `actions/download-artifact@v3`: Download build artifacts

**Custom Actions**: Place in `.forgejo/actions/` within repository

### Secrets Management

**Repository Secrets**:
- Configured in repository settings
- Available via `${{ secrets.SECRET_NAME }}`
- Masked in logs automatically

**Organization Secrets**:
- Shared across all organization repositories
- Managed by organization administrators

**Example**:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        env:
          SSH_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
          SERVER: ${{ secrets.DEPLOY_SERVER }}
        run: |
          echo "$SSH_KEY" > deploy_key
          chmod 600 deploy_key
          scp -i deploy_key ./build/* user@$SERVER:/var/www/
```

### Implementation Notes

**TODO**: Document runner pool sizing after staging performance testing.

**TODO**: Define organizational policies for workflow timeouts and resource limits.

**TODO**: Create template workflows for common technology stacks (Node.js, Python, Java, Go).

---

## 3. Plugin Repositories

### Core Features

**Git Operations**:
- Clone (HTTPS and SSH)
- Push/Pull
- Branch management
- Tag management
- Force push control

**Git LFS**:
- Large file storage backend
- Configurable max file size
- Storage quota per repository/organization

**Branch Protection**:
- Require merge request before merge
- Require status checks to pass
- Require signed commits
- Restrict who can push

### Configuration

**Configuration Section**: `[repository]`

**Key Parameters**:
```ini
[repository]
DEFAULT_BRANCH = main
DEFAULT_PRIVATE = internal
ENABLE_PUSH_CREATE_USER = true
ENABLE_PUSH_CREATE_ORG = true
DISABLED_REPO_UNITS = repo.ext_wiki,repo.projects
DEFAULT_REPO_UNITS = repo.code,repo.releases,repo.issues,repo.pulls,repo.actions

[repository.upload]
ENABLED = true
MAX_FILE_SIZE = 100

[repository.pull-request]
DEFAULT_MERGE_STYLE = merge
ENABLE_AUTO_MERGE = true

[lfs]
ENABLED = true
STORAGE_TYPE = local
PATH = /var/lib/forgejo/data/lfs
MAX_FILE_SIZE = 100
```

### Visibility Levels

| Level | Description | Who Can Access |
|-------|-------------|----------------|
| Private | Hidden from public | Owner and collaborators only |
| Internal | Visible to logged-in users | All authenticated users |
| Public | Publicly accessible | Anyone (including anonymous) |

### Repository Settings

**Per-Repository Configuration**:
- Default branch name
- Description and website URL
- Social preview image
- Archived status (read-only)
- Template repository (use as template for new repos)
- Auto-delete merged branches

**Branch Protection Rules**:
```
Protect branch: main
☑ Enable branch protection
☑ Require pull request reviews before merging
  → Required approving reviews: 1
  → Dismiss stale pull request approvals when new commits are pushed
☑ Require status checks to pass before merging
  → Actions: CI Pipeline
☐ Require signed commits
☑ Include administrators
```

### Implementation Notes

**TODO**: Document organizational standards for repository structure and naming.

**TODO**: Define default branch protection rules for production repositories.

**TODO**: Configure Git LFS storage backend (local vs object storage).

---

## 4. Plugin Registry (Intégration Nexus)

### Overview

Dev-Forge integrates with existing Nexus repository manager to provide unified package management through Forgejo's interface.

**Integration Model**: Proxy/bridge to Nexus (not native Forgejo registry)

### Supported Package Types

| Ecosystem | Nexus Repository Type | Forgejo Endpoint |
|-----------|----------------------|------------------|
| npm | npm (proxy/hosted) | `/api/packages/npm/` |
| Maven | maven2 (proxy/hosted) | `/api/packages/maven/` |
| Docker | docker (hosted) | `/api/packages/docker/` |
| Python (PyPI) | pypi (proxy/hosted) | `/api/packages/pypi/` |
| NuGet | nuget (proxy/hosted) | `/api/packages/nuget/` |

### Configuration

**Configuration Section**: `[packages]`

**Core Settings**:
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
```

**Per-Ecosystem Configuration**:
```ini
[packages.npm]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/npm-group/

[packages.maven]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/maven-public/

[packages.docker]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/docker-hosted/
REGISTRY_HOSTNAME = forge.company.internal

[packages.pypi]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/pypi-group/

[packages.nuget]
ENABLED = true
PROXY_URL = https://nexus.company.internal/repository/nuget-group/
```

### Client Configuration

#### npm

**Configure registry**:
```bash
npm config set registry https://forge.company.internal/api/packages/npm/
```

**Authenticate**:
```bash
npm login --registry=https://forge.company.internal/api/packages/npm/
# Username: <forgejo-username>
# Password: <forgejo-password-or-token>
```

**Publish package**:
```bash
npm publish
```

#### Maven

**In `pom.xml`** or `settings.xml`:
```xml
<repositories>
  <repository>
    <id>devforge</id>
    <url>https://forge.company.internal/api/packages/maven/</url>
  </repository>
</repositories>

<distributionManagement>
  <repository>
    <id>devforge</id>
    <url>https://forge.company.internal/api/packages/maven/</url>
  </repository>
</distributionManagement>
```

**In `~/.m2/settings.xml`**:
```xml
<servers>
  <server>
    <id>devforge</id>
    <username>your-forgejo-username</username>
    <password>your-forgejo-password</password>
  </server>
</servers>
```

#### Docker

**Authenticate**:
```bash
docker login forge.company.internal
# Username: <forgejo-username>
# Password: <forgejo-password-or-token>
```

**Pull image**:
```bash
docker pull forge.company.internal/organization/image:tag
```

**Push image**:
```bash
docker tag myimage:latest forge.company.internal/organization/myimage:latest
docker push forge.company.internal/organization/myimage:latest
```

#### Python (PyPI)

**Configure pip**:
```bash
pip config set global.index-url https://forge.company.internal/api/packages/pypi/simple
```

**Authenticate** (in `~/.pypirc`):
```ini
[distutils]
index-servers = devforge

[devforge]
repository = https://forge.company.internal/api/packages/pypi/
username = your-forgejo-username
password = your-forgejo-password
```

**Publish package**:
```bash
python setup.py sdist bdist_wheel
twine upload --repository devforge dist/*
```

### Authentication Flow

1. Client authenticates to Forgejo (via credentials or API token)
2. Forgejo validates credentials
3. Forgejo generates temporary Nexus user token
4. Request proxied to Nexus with token
5. Nexus returns package data
6. Forgejo forwards response to client

**Token Caching**: 1 hour TTL (configurable)

### Implementation Notes

**TODO**: Document Nexus repository structure and naming conventions.

**TODO**: Configure Nexus user token generation for Forgejo service account.

**TODO**: Test each package ecosystem in staging environment.

**TODO**: Define package retention policies (alignment with Nexus configuration).

---

## 5. Plugin Code Review

### Merge Request Workflow

**Terminology**:
- **Merge Request** (Forgejo/GitLab) ≈ **Pull Request** (GitHub)
- **Approval** ≈ **Review Approval**
- **Changes Requested** ≈ **Request Changes**

**Standard Flow**:
1. Developer creates feature branch
2. Developer pushes commits
3. Developer opens merge request (source → target)
4. Reviewer(s) notified
5. Reviewer adds comments and approval/rejection
6. Developer addresses feedback (pushes new commits)
7. Final approval received
8. Merge request merged (manual or auto-merge)

### Configuration

**Configuration Section**: `[repository.pull-request]`

**Core Settings**:
```ini
[repository.pull-request]
WORK_IN_PROGRESS_PREFIXES = WIP:,[WIP],Draft:
CLOSE_KEYWORDS = close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved
REOPEN_KEYWORDS = reopen,reopens,reopened
DEFAULT_MERGE_STYLE = merge
ENABLE_AUTO_MERGE = true
DEFAULT_MERGE_MESSAGE_COMMITS_LIMIT = 50
DEFAULT_MERGE_MESSAGE_SIZE = 5120
DEFAULT_MERGE_MESSAGE_ALL_AUTHORS = false
DEFAULT_MERGE_MESSAGE_MAX_APPROVERS = 10
POPULATE_SQUASH_COMMENT_WITH_COMMIT_MESSAGES = true
ADD_CO_COMMITTER_TRAILERS = true
```

**Branch Protection**:
```ini
[repository.pull-request.branch-protection]
ENABLE_APPROVALS = true
REQUIRED_APPROVALS = 1
DISMISS_STALE_APPROVALS = true
REQUIRE_SIGNED_COMMITS = false
ENABLE_STATUS_CHECK = true
STATUS_CHECK_CONTEXTS = CI Pipeline
```

### Merge Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Merge** | Creates merge commit | Preserve full history |
| **Rebase** | Rebases and fast-forwards | Linear history |
| **Squash** | Combines all commits into one | Clean history per feature |

**Configuration**:
```ini
[repository.pull-request]
DEFAULT_MERGE_STYLE = merge
ENABLE_MERGE_WHITELIST = true
ENABLE_REBASE_MERGE = true
ENABLE_SQUASH_MERGE = true
```

### Review Features

**Inline Comments**:
- Comment on specific lines
- Start discussions
- Resolve conversations when addressed

**Review States**:
- **Comment**: General feedback without approval status
- **Approve**: Satisfies review requirements
- **Request Changes**: Blocks merge until addressed

**Code Suggestions**:
```
Suggested change:
-  if (user = null) {
+  if (user === null) {
```

### Notifications

**Events Triggering Notifications**:
- Merge request opened
- New commits pushed
- Review requested
- Comment added
- Approval given
- Changes requested
- Merge request merged/closed

**Notification Channels**:
- Web UI (bell icon)
- Email (configurable per user)
- Webhook (for external integrations)

**Configuration**:
```ini
[webhook]
ALLOWED_HOST_LIST = *
SKIP_TLS_VERIFY = false

[mailer]
ENABLED = true
FROM = forgejo@company.internal
PROTOCOL = smtp
SMTP_ADDR = smtp.company.internal
SMTP_PORT = 587
```

### Auto-Merge

**Requirements for Auto-Merge**:
- All required approvals received
- All status checks passed (CI/CD)
- No merge conflicts
- Branch protection rules satisfied

**Behavior**:
- Automatically merges when conditions met
- Can be enabled per merge request
- Respects merge strategy configuration

### Integration with Actions

**Status Check Integration**:
```yaml
name: CI Pipeline

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test
```

**Status visible in merge request**:
- ✅ CI Pipeline: passed
- ⏳ CI Pipeline: running
- ❌ CI Pipeline: failed

### Implementation Notes

**TODO**: Define organizational code review standards and etiquette.

**TODO**: Document internal vs external contributor workflows.

**TODO**: Configure default reviewers/CODEOWNERS files for key repositories.

**TODO**: Set up merge request templates for consistent descriptions.

---

## 6. Plugin Pages

### Overview

Forgejo Pages enables hosting of static websites directly from Git repositories, similar to GitHub Pages. Ideal for project documentation, API references, demos, and landing pages.

### Configuration

**Configuration Section**: `[server]` and repository-level settings

**Global Settings** (app.ini):
```ini
[server]
ENABLE_PAGES = true
ROOT_URL = https://forgejo.company.internal/
PAGES_URL = https://pages.company.internal/
```

**Per-Repository Settings**:
- Enable Pages in repository settings
- Select branch (e.g., `gh-pages`, `main`) and optionally path (e.g., `/docs`)
- Optional: Configure custom domain via CNAME file

### Supported Static Site Generators

**Tested Frameworks**:
- **Jekyll**: Ruby-based, GitHub Pages standard
- **Hugo**: Go-based, fast builds
- **MkDocs**: Python-based, documentation-focused
- **Docusaurus**: React-based, modern docs sites
- **VuePress**: Vue.js-based
- **Plain HTML/CSS/JS**: No framework required

### Deployment Workflow

**Automatic Deployment**:
1. Developer pushes to configured Pages branch (e.g., `gh-pages`)
2. Forgejo detects commit to Pages branch
3. Site automatically deployed to `https://pages.company.internal/<user>/<repo>/`
4. Changes visible within seconds

**Build Process** (optional):
- Use Forgejo Actions workflow to build static site
- Push build output to Pages branch
- Forgejo serves pre-built artifacts

**Example workflow** (`.forgejo/workflows/deploy-docs.yml`):
```yaml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: cd docs && npm install
      
      - name: Build static site
        run: cd docs && npm run build
      
      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.FORGEJO_TOKEN }}
          publish_dir: ./docs/build
          publish_branch: gh-pages
```

### Custom Domains

**Setup Process**:
1. Create `CNAME` file in Pages branch root containing domain: `docs.project.company.internal`
2. Configure DNS: CNAME record pointing to Forgejo Pages server
3. Pages site accessible at custom domain with HTTPS

**Example CNAME file**:
```
docs.myproject.company.internal
```

### Access Control

**Public Repositories**:
- Pages site publicly accessible (if Forgejo instance allows anonymous access)
- Suitable for open-source project documentation

**Private Repositories**:
- Pages site requires authentication
- Users must have repository read access to view site
- Suitable for internal documentation

### URL Structure

**Default URLs**:
- User repository: `https://pages.company.internal/<username>/<repo>/`
- Organization repository: `https://pages.company.internal/<org>/<repo>/`
- Custom domain: `https://docs.project.company.internal/`

**Branch/Path Configuration**:
- Branch only: Serves root of branch
- Branch + path: Serves content from specified path (e.g., `main/docs/`)

### Troubleshooting

**Common Issues**:

**Site not updating**:
- Verify Pages enabled in repository settings
- Check configured branch name matches actual branch
- Review commit history on Pages branch
- Clear browser cache

**404 errors**:
- Ensure `index.html` exists in configured path
- Check directory structure matches configured path
- Verify file permissions (all files must be readable)

**Build failures** (when using Actions):
- Review workflow logs for build errors
- Ensure build output directory matches `publish_dir` configuration
- Verify Actions workflow has correct permissions

### Security Considerations

**Content Security**:
- Pages serve only static content (HTML, CSS, JS, images)
- No server-side code execution (PHP, Python, etc.)
- JavaScript executed in user's browser (same origin restrictions apply)

**Authentication**:
- Private repository Pages require Forgejo authentication
- No separate Pages-specific authentication

**HTTPS**:
- All Pages sites served over HTTPS (enforced)
- Custom domains require valid SSL certificate

### Implementation Notes

**Storage**: Pages content served directly from Git repository (no separate storage). This ensures:
- Version control for all content
- Easy rollback via Git
- Audit trail for changes

**Performance**: Consider enabling CDN or reverse proxy caching for frequently accessed documentation sites.

**Limits**: Set reasonable repository size limits (e.g., 1 GB) and file count limits to prevent abuse.

**TODO**: Document organizational guidelines for Pages usage (acceptable content, naming conventions).

**TODO**: Set up monitoring for Pages deployment success/failure rates.

---

## Plugin Interaction Matrix

| From Plugin | To Plugin | Interaction | Example |
|-------------|-----------|-------------|---------|
| Authentication | Actions | User identity for workflows | Workflow triggered by authenticated push |
| Authentication | Repositories | Access control | User authorization for git operations |
| Authentication | Pages | Access control for private sites | User must authenticate to view private repo documentation |
| Repositories | Actions | Workflow triggers | Push to branch triggers pipeline |
| Repositories | Code Review | Merge requests | Developer creates MR from branch |
| Repositories | Pages | Content source | Pages serves static content from repository branch |
| Actions | Code Review | Status checks | CI result blocks/allows merge |
| Actions | Registry | Publish artifacts | Pipeline publishes package to registry |
| Actions | Pages | Site deployment | Workflow builds static site and pushes to Pages branch |
| Registry | Repositories | Dependency resolution | Workflow installs dependencies from registry |

---

## Next Plugin Phases (Future)

**Phase 2 Candidates**:
- Issue tracking and project management
- Wiki and documentation
- Advanced security scanning (SAST/DAST)
- Metrics and observability integration

**Phase 3 Candidates**:
- Advanced deployment automation (Kubernetes, Terraform)
- Policy enforcement (commit signing, vulnerability scanning)
- Advanced analytics and reporting

---

## Voir Aussi

- [Guide Pratique : Configurer les Plugins](../guide-pratique/configurer-plugins.md) — Procédures activation et configuration
- [Explication : Sélection Plugins MVP (ADR-0004)](../../ADR/0004-plugins-mvp.md) — Justification choix plugins
- [Référence : Configuration Forgejo](configuration-forgejo.md) — Référence configuration complète

---

## Navigation

📚 **Autre Référence** : [Configuration Forgejo](configuration-forgejo.md)  
⬆️ [Retour aux Références](../reference/)  
🔧 [Guides Pratiques](../guide-pratique/) | 📖 [Tutoriels](../tutoriel/)

> **Note** : Ce document contient du contenu technique détaillé en anglais. Une traduction complète est en cours.
