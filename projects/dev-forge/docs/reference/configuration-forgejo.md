# Référence : Configuration Forgejo

Référence complète des paramètres de configuration Forgejo (`app.ini`) pertinents pour le déploiement Dev-Forge.

---

## Emplacement du Fichier de Configuration

**Chemin par Défaut** : `/etc/forgejo/app.ini`

**Chemin de Remplacement** (variable d'environnement) : `FORGEJO_CUSTOM`

**Format** : Format INI avec sections et paires clé-valeur

---

## Sections de Configuration Principales

### `[server]` — Paramètres du Serveur Web

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

**Paramètres Clés** :
- `PROTOCOL` : `http` | `https` | `unix` | `fcgi`
- `DOMAIN` : Nom d'hôte (sans protocole ni port)
- `ROOT_URL` : URL de base complète (doit correspondre à la configuration HTTPS)
- `HTTP_PORT` : Port d'écoute interne (typiquement 3000, proxifié)
- `OFFLINE_MODE` : `true` désactive les ressources externes (Gravatar, etc.)

---

### `[database]` — Connexion Base de Données

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

**`DB_TYPE` Supportés** :
- `postgres` (recommandé pour production)
- `mysql` / `mariadb`
- `mssql`
- `sqlite3` (développement uniquement)

**Pooling de Connexion** :
- `MAX_IDLE_CONNS` : Connexions keep-alive (2 pour faible trafic)
- `MAX_OPEN_CONNS` : Connexions simultanées maximum (0 = illimité)

---

### `[security]` — Authentification & Sécurité

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

**Paramètres Critiques** :
- `SECRET_KEY` : Utilisé pour chiffrement cookies (DOIT être unique par installation)
- `INTERNAL_TOKEN` : Authentification API entre services
- `PASSWORD_HASH_ALGO` : `pbkdf2` | `argon2` | `scrypt` | `bcrypt`

**Générer les Secrets** :
```bash
forgejo generate secret SECRET_KEY
forgejo generate secret INTERNAL_TOKEN
```

---

### `[service]` — Inscription Utilisateur & Comportement

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

**Contrôles d'Inscription** :
- `DISABLE_REGISTRATION` : `true` = création utilisateur par admin uniquement
- `REGISTER_EMAIL_CONFIRM` : Exiger vérification email

**Visibilité** :
- `REQUIRE_SIGNIN_VIEW` : Forcer connexion pour voir tout contenu

---

### `[repository]` — Paramètres par Défaut des Dépôts

Voir [Référence Plugins MVP — Repositories](plugins-mvp.md#3-repositories-plugin) pour détails complets.

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

### `[actions]` — Configuration CI/CD

Voir [Référence Plugins MVP — Actions](plugins-mvp.md#2-actions-plugin-cicd) pour détails complets.

```ini
[actions]
ENABLED = true
DEFAULT_ACTIONS_URL = https://code.forgejo.org
```

---

### `[packages]` — Registry de Packages

Voir [Référence Plugins MVP — Registry](plugins-mvp.md#4-registry-plugin-nexus-integration) pour détails complets.

```ini
[packages]
ENABLED = true

[packages.proxy]
TYPE = nexus
URL = https://nexus.company.internal
```

---

### `[mailer]` — Notifications Email

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

**Protocoles** :
- `smtp` : SMTP standard
- `smtps` : SMTP over TLS (port 465)
- `smtp+starttls` : SMTP avec STARTTLS (port 587)
- `sendmail` : Utiliser binaire sendmail local
- `dummy` : Désactiver envoi (log uniquement)

---

### `[session]` — Gestion de Session

```ini
[session]
PROVIDER = db
PROVIDER_CONFIG = data/sessions
COOKIE_SECURE = true
COOKIE_NAME = i_like_forgejo
GC_INTERVAL_TIME = 86400
SESSION_LIFE_TIME = 86400
```

**Providers** :
- `db` : Stockage base de données (recommandé)
- `file` : Stockage système de fichiers
- `memory` : En mémoire (développement uniquement)
- `redis` : Backend Redis

**Sécurité** :
- `COOKIE_SECURE` : `true` requiert HTTPS
- `SESSION_LIFE_TIME` : Timeout session (secondes)

---

### `[oauth2]` — Fournisseur OAuth2 (Forgejo comme IdP)

**Note** : Séparé de `[oauth2_client]` (Forgejo comme consommateur OAuth2)

```ini
[oauth2]
ENABLE = true
JWT_SECRET = <random-jwt-secret>
JWT_SIGNING_ALGORITHM = HS256
```

**Cas d'Usage** : Permettre aux applications externes de s'authentifier via Forgejo

---

### `[log]` — Configuration Logging

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

**Niveaux Log** : `Trace` | `Debug` | `Info` | `Warn` | `Error` | `Critical`

**Modes** : `console` | `file` | `syslog` | `smtp`

---

### `[metrics]` — Métriques Prometheus

```ini
[metrics]
ENABLED = true
TOKEN = <metrics-auth-token>
```

**Endpoint** : `https://forge.company.internal/metrics`

**Authentification** : Requiert header `Authorization: Bearer <TOKEN>`

---

### `[cache]` — Backend Caching

```ini
[cache]
ADAPTER = memory
INTERVAL = 60
HOST = 127.0.0.1:6379

[cache.last_commit]
ENABLED = true
COMMITS_COUNT = 100
```

**Adapters** :
- `memory` : En mémoire (simple, pas de persistance)
- `redis` : Backend Redis (recommandé multi-instance)
- `memcache` : Backend Memcached

---

## Paramètres Spécifiques à l'Environnement

### Environnement Staging

**Différences Clés vs Production** :
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

### Environnement Production

**Différences Clés** :
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

## Validation de Configuration

### Vérifier la Syntaxe

```bash
forgejo --config /etc/forgejo/app.ini --check
```

### Vérifier Connexion Base de Données

```bash
forgejo --config /etc/forgejo/app.ini doctor check --run database
```

### Afficher Configuration Effective

```bash
forgejo admin show-config
```

---

## Bonnes Pratiques de Configuration

1. **Gestion des Secrets** : Ne jamais commiter `app.ini` avec secrets dans contrôle de version
2. **Variables d'Environnement** : Remplacer valeurs sensibles via format `FORGEJO__SECTION__KEY`
3. **Validation** : Toujours exécuter `--check` après édition configuration
4. **Sauvegardes** : Inclure `app.ini` dans procédures de backup
5. **Documentation** : Commenter les paramètres non-évidents pour futurs mainteneurs

---

## Voir Aussi

- [Référence : Plugins MVP](plugins-mvp.md) — Détails configuration plugins
- [Guide Pratique : Configurer les Plugins](../guide-pratique/configurer-plugins.md) — Procédures configuration
- Documentation Officielle Forgejo : https://forgejo.org/docs/

---

## Navigation

📚 **Autre Référence** : [Plugins MVP](plugins-mvp.md)  
⬆️ [Retour aux Références](../reference/)  
🔧 [Guides Pratiques](../guide-pratique/) | 📖 [Tutoriels](../tutoriel/)
