# Reference: Forgejo Configuration

Complete reference for Forgejo (`app.ini`) configuration parameters relevant to Dev-Forge deployment.

---

## Configuration File Location

**Default Path**: `/etc/forgejo/app.ini`

**Override Path** (environment variable): `FORGEJO_CUSTOM`

**Format**: INI format with sections and key-value pairs

---

## Core Configuration Sections

### `[server]` — Web Server Settings

```ini
[server]
PROTOCOL = https
DOMAIN = forge.company.internal
ROOT_URL = https://forge.company.internal/
HTTP_PORT = 3000
REDIRECT_OTHER_PORT = true
PORT_TO_REDIRECT = 80
CERT_FILE = /etc/forgejo/cert.pem
KEY_FILE = /etc/forgejo/key.pem
SSH_DOMAIN = forge.company.internal
SSH_PORT = 22
START_SSH_SERVER = true
OFFLINE_MODE = false
LFS_START_SERVER = true
```

**Key Parameters**:
- `PROTOCOL`: `http` | `https` | `unix` | `fcgi`
- `DOMAIN`: Hostname (without protocol or port)
- `ROOT_URL`: Full base URL (must match HTTPS configuration)
- `HTTP_PORT`: Internal listen port (typically 3000, proxied)
- `OFFLINE_MODE`: `true` disables external resources (Gravatar, etc.)

---

### `[database]` — Database Connection

```ini
[database]
DB_TYPE = postgres
HOST = db.company.internal:5432
NAME = forgejo
USER = forgejo
PASSWD = SecurePassword123
SCHEMA = public
SSL_MODE = require
LOG_SQL = false
MAX_IDLE_CONNS = 2
MAX_OPEN_CONNS = 0
CONN_MAX_LIFETIME = 3s
```

**Supported `DB_TYPE`**:
- `postgres` (recommended for production)
- `mysql` / `mariadb`
- `mssql`
- `sqlite3` (development only)

**Connection Pooling**:
- `MAX_IDLE_CONNS`: Keep-alive connections (2 for low traffic)
- `MAX_OPEN_CONNS`: Maximum simultaneous connections (0 = unlimited)

---

### `[security]` — Authentication & Security

```ini
[security]
INSTALL_LOCK = true
SECRET_KEY = <random-64-character-string>
INTERNAL_TOKEN = <random-authentication-token>
PASSWORD_HASH_ALGO = argon2
MIN_PASSWORD_LENGTH = 8
PASSWORD_COMPLEXITY = lower,upper,digit
REVERSE_PROXY_LIMIT = 1
REVERSE_PROXY_TRUSTED_PROXIES = 10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

**Critical Parameters**:
- `SECRET_KEY`: Used for cookie encryption (MUST be unique per installation)
- `INTERNAL_TOKEN`: API authentication between services
- `PASSWORD_HASH_ALGO`: `pbkdf2` | `argon2` | `scrypt` | `bcrypt`

**Generate Secrets**:
```bash
forgejo generate secret SECRET_KEY
forgejo generate secret INTERNAL_TOKEN
```

---

### `[service]` — User Registration & Behavior

```ini
[service]
REGISTER_EMAIL_CONFIRM = false
DISABLE_REGISTRATION = true
REQUIRE_SIGNIN_VIEW = true
ENABLE_NOTIFY_MAIL = true
DEFAULT_KEEP_EMAIL_PRIVATE = true
DEFAULT_ALLOW_CREATE_ORGANIZATION = true
DEFAULT_ENABLE_TIMETRACKING = false
ENABLE_USER_HEATMAP = true
```

**Registration Controls**:
- `DISABLE_REGISTRATION`: `true` = admin-only user creation
- `REGISTER_EMAIL_CONFIRM`: Require email verification

**Visibility**:
- `REQUIRE_SIGNIN_VIEW`: Force login to view any content

---

### `[repository]` — Repository Defaults

See [MVP Plugins Reference — Repositories](plugins-mvp.md#3-repositories-plugin) for complete details.

```ini
[repository]
DEFAULT_BRANCH = main
DEFAULT_PRIVATE = internal
ENABLE_PUSH_CREATE_USER = true
ENABLE_PUSH_CREATE_ORG = true
DEFAULT_REPO_UNITS = repo.code,repo.releases,repo.issues,repo.pulls,repo.actions

[repository.upload]
MAX_FILE_SIZE = 100

[repository.pull-request]
DEFAULT_MERGE_STYLE = merge
ENABLE_AUTO_MERGE = true
```

---

### `[actions]` — CI/CD Configuration

See [MVP Plugins Reference — Actions](plugins-mvp.md#2-actions-plugin-cicd) for complete details.

```ini
[actions]
ENABLED = true
DEFAULT_ACTIONS_URL = https://code.forgejo.org
```

---

### `[packages]` — Package Registry

See [MVP Plugins Reference — Registry](plugins-mvp.md#4-registry-plugin-nexus-integration) for complete details.

```ini
[packages]
ENABLED = true

[packages.proxy]
TYPE = nexus
URL = https://nexus.company.internal
```

---

### `[mailer]` — Email Notifications

```ini
[mailer]
ENABLED = true
FROM = forgejo@company.internal
PROTOCOL = smtp
SMTP_ADDR = smtp.company.internal
SMTP_PORT = 587
USER = forgejo@company.internal
PASSWD = EmailPassword123
ENABLE_HELO = true
HELO_HOSTNAME = forge.company.internal
```

**Protocols**:
- `smtp`: Standard SMTP
- `smtps`: SMTP over TLS (port 465)
- `smtp+starttls`: SMTP with STARTTLS (port 587)
- `sendmail`: Use local sendmail binary
- `dummy`: Disable sending (log only)

---

### `[session]` — Session Management

```ini
[session]
PROVIDER = db
PROVIDER_CONFIG = data/sessions
COOKIE_SECURE = true
COOKIE_NAME = i_like_forgejo
GC_INTERVAL_TIME = 86400
SESSION_LIFE_TIME = 86400
```

**Providers**:
- `db`: Database storage (recommended)
- `file`: Filesystem storage
- `memory`: In-memory (development only)
- `redis`: Redis backend

**Security**:
- `COOKIE_SECURE`: `true` requires HTTPS
- `SESSION_LIFE_TIME`: Session timeout (seconds)

---

### `[oauth2]` — OAuth2 Provider (Forgejo as IdP)

**Note**: Separate from `[oauth2_client]` (Forgejo as OAuth2 consumer)

```ini
[oauth2]
ENABLE = true
JWT_SECRET = <random-jwt-secret>
JWT_SIGNING_ALGORITHM = HS256
```

**Use Case**: Allow external applications to authenticate via Forgejo

---

### `[log]` — Logging Configuration

```ini
[log]
MODE = console,file
LEVEL = Info
ROOT_PATH = /var/log/forgejo

[log.console]
LEVEL = Info
STDERR = false

[log.file]
LEVEL = Info
FILE_NAME = forgejo.log
MAX_SIZE_SHIFT = 28
LOG_ROTATE = true
DAILY_ROTATE = true
MAX_DAYS = 7
COMPRESS = true
```

**Log Levels**: `Trace` | `Debug` | `Info` | `Warn` | `Error` | `Critical`

**Modes**: `console` | `file` | `syslog` | `smtp`

---

### `[metrics]` — Prometheus Metrics

```ini
[metrics]
ENABLED = true
TOKEN = <metrics-auth-token>
```

**Endpoint**: `https://forge.company.internal/metrics`

**Authentication**: Requires `Authorization: Bearer <TOKEN>` header

---

### `[cache]` — Caching Backend

```ini
[cache]
ADAPTER = memory
INTERVAL = 60
HOST = 127.0.0.1:6379

[cache.last_commit]
ENABLED = true
COMMITS_COUNT = 100
```

**Adapters**:
- `memory`: In-memory (simple, no persistence)
- `redis`: Redis backend (recommended for multi-instance)
- `memcache`: Memcached backend

---

## Environment-Specific Settings

### Staging Environment

**Key Differences from Production**:
```ini
[server]
DOMAIN = forge-staging.company.internal
ROOT_URL = https://forge-staging.company.internal/

[security]
# Separate secrets per environment
SECRET_KEY = <staging-specific-secret>
INTERNAL_TOKEN = <staging-specific-token>

[database]
HOST = db-staging.company.internal:5432
NAME = forgejo_staging

[actions]
# Smaller runner pool in staging
```

### Production Environment

**Key Differences**:
```ini
[server]
DOMAIN = forge.company.internal
ROOT_URL = https://forge.company.internal/

[security]
# Production secrets
SECRET_KEY = <production-specific-secret>
INTERNAL_TOKEN = <production-specific-token>

[database]
HOST = db-prod.company.internal:5432
NAME = forgejo_production
MAX_OPEN_CONNS = 100

[log]
LEVEL = Warn
MAX_DAYS = 30
```

---

## Configuration Validation

### Check Syntax

```bash
forgejo --config /etc/forgejo/app.ini --check
```

### Verify Database Connection

```bash
forgejo --config /etc/forgejo/app.ini doctor check --run database
```

### Display Effective Configuration

```bash
forgejo admin show-config
```

---

## Configuration Best Practices

1. **Secrets Management**: Never commit `app.ini` with secrets to version control
2. **Environment Variables**: Override sensitive values via `FORGEJO__SECTION__KEY` format
3. **Validation**: Always run `--check` after editing configuration
4. **Backups**: Include `app.ini` in backup procedures
5. **Documentation**: Comment non-obvious settings for future maintainers

---

## See Also

- [Reference: MVP Plugins](plugins-mvp.md) — Plugin-specific configuration details
- [How-To: Setup Plugins](../how-to/setup-plugins.md) — Configuration procedures
- Official Forgejo Documentation: https://forgejo.org/docs/
