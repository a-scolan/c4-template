# How-To: Setup Dev-Forge Plugins

This guide shows you how to activate and configure the MVP plugins that power Dev-Forge functionality.

---

## Prerequisites

- Administrator access to Forgejo instance
- Access to Forgejo configuration file (`app.ini`)
- Understanding of Dev-Forge architecture (see [ADR-0004: MVP Plugins](../../ADR/0004-mvp-plugins.md))

---

## Understanding MVP Plugins

Dev-Forge's MVP consists of five essential plugin categories:

1. **Authentication** — LDAP/OIDC integration
2. **Actions** — CI/CD automation
3. **Repositories** — Git hosting and management
4. **Registry** — Package management via Nexus
5. **Code Review** — Merge request workflows

Each plugin is configured via Forgejo's `app.ini` configuration file and may require service restart.

---

## Activate Authentication Plugin

### Choose Authentication Method

Dev-Forge supports two authentication backends:

- **LDAP**: Corporate directory integration
- **OIDC**: Modern SSO provider (Keycloak, Auth0, etc.)

### Configure LDAP Authentication

**If your organization uses Active Directory or LDAP**:

1. Edit Forgejo configuration:
   ```bash
   sudo nano /etc/forgejo/app.ini
   ```

2. Add LDAP authentication section:
   ```ini
   [auth]
   ENABLE_LDAP = true
   
   [auth.ldap.default]
   NAME = Corporate LDAP
   ENABLED = true
   HOST = ldap.company.internal
   PORT = 389
   SECURITY_PROTOCOL = unencrypted
   BIND_DN = cn=forgejo,ou=services,dc=company,dc=internal
   BIND_PASSWORD = <service_account_password>
   USER_BASE = ou=users,dc=company,dc=internal
   USER_FILTER = (uid=%s)
   ADMIN_FILTER = (memberOf=cn=forgejo-admins,ou=groups,dc=company,dc=internal)
   USERNAME_ATTRIBUTE = uid
   EMAIL_ATTRIBUTE = mail
   ```

3. Restart Forgejo:
   ```bash
   sudo systemctl restart forgejo
   ```

4. Test authentication:
   - Navigate to Forgejo login page
   - Use corporate LDAP credentials
   - Verify user profile populated from LDAP

### Configure OIDC Authentication

**If your organization uses SSO provider**:

1. Edit configuration:
   ```bash
   sudo nano /etc/forgejo/app.ini
   ```

2. Add OIDC section:
   ```ini
   [oauth2_client]
   ENABLE_AUTO_REGISTRATION = true
   
   [oauth2.keycloak]
   NAME = Corporate SSO
   ENABLED = true
   CLIENT_ID = forgejo
   CLIENT_SECRET = <oidc_client_secret>
   OPENID_CONNECT_AUTO_DISCOVERY_URL = https://sso.company.internal/auth/realms/company/.well-known/openid-configuration
   ```

3. Restart and test as above

---

## Activate Actions Plugin

Forgejo Actions is enabled by default but requires runner configuration.

### Verify Actions Enabled

1. Check configuration:
   ```bash
   grep -A5 "\[actions\]" /etc/forgejo/app.ini
   ```

2. Expected output:
   ```ini
   [actions]
   ENABLED = true
   DEFAULT_ACTIONS_URL = https://code.forgejo.org
   ```

3. If missing, add the section and restart Forgejo

### Register Runners

Runners must be registered before workflows can execute:

1. Generate registration token:
   - Navigate to **Site Administration** → **Actions** → **Runners**
   - Click **"Create registration token"**
   - Copy token (shown once)

2. Expected Puppet configuration (automated registration):
   ```puppet
   forgejo_runner::register { 'runner-1':
     token => '<registration_token>',
     labels => ['ubuntu-latest', 'docker'],
   }
   ```

3. Verify runners appear in admin panel with "idle" status

See [Configure Runners](configure-runners.md) for detailed runner management.

---

## Activate Repository Management

Repository features are core to Forgejo and enabled by default.

### Configure Repository Settings

1. Set repository defaults:
   ```ini
   [repository]
   DEFAULT_BRANCH = main
   DEFAULT_PRIVATE = internal
   ENABLE_PUSH_CREATE_USER = true
   ENABLE_PUSH_CREATE_ORG = true
   DISABLED_REPO_UNITS = repo.ext_wiki,repo.projects
   ```

2. Configure Git LFS (large file storage):
   ```ini
   [lfs]
   ENABLED = true
   STORAGE_TYPE = local
   PATH = /var/lib/forgejo/data/lfs
   ```

3. Set limits:
   ```ini
   [repository.upload]
   MAX_FILE_SIZE = 100
   
   [repository.pull-request]
   DEFAULT_MERGE_STYLE = merge
   ```

4. Restart Forgejo

### Verify Repository Features

Test repository operations:
```bash
# Create test repository
curl -X POST "https://forge.company.internal/api/v1/user/repos" \
  -H "Authorization: token <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"test-repo","private":true}'

# Clone and test
git clone https://forge.company.internal/admin/test-repo.git
cd test-repo
echo "Test" > test.txt
git add test.txt
git commit -m "Test commit"
git push origin main
```

---

## Activate Package Registry (Nexus Integration)

Dev-Forge integrates with your existing Nexus instance for package management.

### Configure Registry Bridge

**Note**: This creates a proxy/bridge to Nexus, not a native Forgejo registry.

1. Enable package registry:
   ```ini
   [packages]
   ENABLED = true
   
   [packages.proxy]
   TYPE = nexus
   URL = https://nexus.company.internal
   ```

2. Configure per-ecosystem registry endpoints:
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
   ```

3. Configure authentication passthrough:
   ```ini
   [packages.auth]
   NEXUS_TOKEN_URL = https://nexus.company.internal/service/rest/v1/security/user-tokens
   ```

4. Restart Forgejo

### Test Registry Integration

**For npm**:
```bash
npm config set registry https://forge.company.internal/api/packages/npm/
npm login --registry=https://forge.company.internal/api/packages/npm/
npm install express
```

**For Maven**:
```xml
<!-- In pom.xml -->
<repositories>
  <repository>
    <id>devforge</id>
    <url>https://forge.company.internal/api/packages/maven/</url>
  </repository>
</repositories>
```

**For Docker**:
```bash
docker login forge.company.internal
docker pull forge.company.internal/library/alpine:latest
```

---

## Activate Code Review Plugin

Code review functionality includes merge requests (pull requests) and approval workflows.

### Configure Code Review Settings

1. Enable and configure merge requests:
   ```ini
   [repository.pull-request]
   WORK_IN_PROGRESS_PREFIXES = WIP:,[WIP],Draft:
   CLOSE_KEYWORDS = close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved
   REOPEN_KEYWORDS = reopen,reopens,reopened
   DEFAULT_MERGE_STYLE = merge
   ENABLE_AUTO_MERGE = true
   ```

2. Configure approval requirements:
   ```ini
   [repository.pull-request.branch-protection]
   ENABLE_APPROVALS = true
   REQUIRED_APPROVALS = 1
   DISMISS_STALE_APPROVALS = true
   REQUIRE_SIGNED_COMMITS = false
   ```

3. Configure review notifications:
   ```ini
   [webhook]
   ALLOWED_HOST_LIST = *
   
   [mailer]
   ENABLED = true
   FROM = forgejo@company.internal
   PROTOCOL = smtp
   SMTP_ADDR = smtp.company.internal
   SMTP_PORT = 587
   ```

4. Restart Forgejo

### Verify Code Review Workflow

Test merge request process:

1. Create a branch:
   ```bash
   git checkout -b feature/test-review
   echo "Feature code" > feature.txt
   git add feature.txt
   git commit -m "Add feature"
   git push origin feature/test-review
   ```

2. Open merge request in Forgejo web interface:
   - Navigate to repository
   - Click **"New Pull Request"**
   - Select `feature/test-review` → `main`
   - Add description and create request

3. Request review from team member

4. Verify:
   - Reviewer receives notification
   - Reviewer can comment on code
   - Approval required before merge
   - Auto-merge option available

---

## Verify Complete Plugin Configuration

### Health Check Checklist

Run through this checklist to verify all MVP plugins are functional:

- [ ] **Authentication**: Can log in via LDAP/OIDC
- [ ] **Actions**: Workflow executes successfully
- [ ] **Repositories**: Can create, clone, push, pull
- [ ] **Registry**: Can pull package via Nexus bridge
- [ ] **Code Review**: Can create and merge pull request

### Generate Configuration Report

```bash
# Generate summary of active plugins
sudo forgejo admin show-config | grep -E "(ENABLED|auth|actions|packages|repository.pull-request)"
```

---

## Troubleshooting

### Authentication Not Working

**LDAP issues**:
- Test LDAP bind: `ldapsearch -x -H ldap://ldap.company.internal -D "cn=forgejo,ou=services,dc=company,dc=internal" -W -b "ou=users,dc=company,dc=internal"`
- Verify firewall allows port 389 (LDAP) or 636 (LDAPS)
- Check bind credentials in `app.ini`

**OIDC issues**:
- Verify auto-discovery URL accessible: `curl https://sso.company.internal/.../.well-known/openid-configuration`
- Check client ID and secret match provider configuration
- Verify redirect URI registered: `https://forge.company.internal/user/oauth2/keycloak/callback`

### Actions Not Triggering

- Verify Actions enabled: `grep ENABLED /etc/forgejo/app.ini | grep actions`
- Check runners registered: Web UI → Site Administration → Actions → Runners
- Review webhook delivery: Repository → Settings → Webhooks → Recent Deliveries

### Registry Returns 404

- Verify Nexus instance reachable from Forgejo server
- Check proxy URL configuration matches Nexus repository paths
- Test direct Nexus access: `curl -I https://nexus.company.internal/repository/npm-group/`

### Merge Request Approvals Not Enforced

- Check branch protection enabled for target branch (usually `main`)
- Verify `REQUIRED_APPROVALS` set correctly
- Ensure reviewer has appropriate permissions (Write or Admin)

---

## Next Steps

- **Customize workflows**: Adapt plugin configuration to organizational policies
- **Monitor usage**: Track plugin adoption and performance
- **Plan extensions**: Identify additional plugins for future phases

## Related Documentation

- [Reference: MVP Plugins](../reference/plugins-mvp.md) — Detailed plugin specifications
- [Explanation: Plugin Selection (ADR-0004)](../../ADR/0004-mvp-plugins.md) — Architectural rationale
- [Reference: Forgejo Configuration](../reference/forgejo-config.md) — Complete configuration reference
