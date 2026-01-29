# Guide Pratique : Configurer les Plugins Dev-Forge

Ce guide vous montre comment activer et configurer les plugins MVP qui alimentent les fonctionnalités de Dev-Forge.

---

## Prérequis

- Accès administrateur à l'instance Forgejo
- Accès au fichier de configuration Forgejo (`app.ini`)
- Compréhension de l'architecture Dev-Forge (voir [ADR-0004 : Plugins MVP](../../ADR/0004-plugins-mvp.md))

---

## Comprendre les Plugins MVP

Le MVP de Dev-Forge consiste en six catégories de plugins essentiels :

1. **Authentication** — Intégration LDAP/OIDC
2. **Actions** — Automatisation CI/CD
3. **Repositories** — Hébergement et gestion Git
4. **Registry** — Gestion de packages via Nexus
5. **Code Review** — Workflows de merge requests
6. **Pages** — Hébergement de sites statiques

Chaque plugin est configuré via le fichier de configuration `app.ini` de Forgejo et peut nécessiter un redémarrage du service.

---

## Activer le Plugin d'Authentification

### Choisir la Méthode d'Authentification

Dev-Forge supporte deux backends d'authentification :

- **LDAP** : Intégration avec l'annuaire d'entreprise
- **OIDC** : Fournisseur SSO moderne (Keycloak, Auth0, etc.)

### Configurer l'Authentification LDAP

**Si votre organisation utilise Active Directory ou LDAP** :

1. Éditer la configuration Forgejo :
   ```bash
   sudo nano /etc/forgejo/app.ini
   ```

2. Ajouter la section d'authentification LDAP :
   ```ini
   [auth]
   ENABLE_LDAP = true
   
   [auth.ldap.default]
   NAME = LDAP d'Entreprise
   ENABLED = true
   HOST = ldap.entreprise.internal
   PORT = 389
   SECURITY_PROTOCOL = unencrypted
   BIND_DN = cn=forgejo,ou=services,dc=entreprise,dc=internal
   BIND_PASSWORD = <mot_de_passe_compte_service>
   USER_BASE = ou=users,dc=entreprise,dc=internal
   USER_FILTER = (uid=%s)
   ADMIN_FILTER = (memberOf=cn=forgejo-admins,ou=groups,dc=entreprise,dc=internal)
   USERNAME_ATTRIBUTE = uid
   EMAIL_ATTRIBUTE = mail
   ```

3. Redémarrer Forgejo :
   ```bash
   sudo systemctl restart forgejo
   ```

4. Tester l'authentification :
   - Naviguer vers la page de connexion Forgejo
   - Utiliser les identifiants LDAP d'entreprise
   - Vérifier que le profil utilisateur est rempli depuis LDAP

### Configurer l'Authentification OIDC

**Si votre organisation utilise un fournisseur SSO** :

1. Éditer la configuration :
   ```bash
   sudo nano /etc/forgejo/app.ini
   ```

2. Ajouter la section OIDC :
   ```ini
   [oauth2_client]
   ENABLE_AUTO_REGISTRATION = true
   
   [oauth2.keycloak]
   NAME = SSO d'Entreprise
   ENABLED = true
   CLIENT_ID = forgejo
   CLIENT_SECRET = <secret_client_oidc>
   OPENID_CONNECT_AUTO_DISCOVERY_URL = https://sso.entreprise.internal/auth/realms/entreprise/.well-known/openid-configuration
   ```

3. Redémarrer et tester comme ci-dessus

---

## Activer le Plugin Actions

Forgejo Actions est activé par défaut mais nécessite configuration des runners.

### Vérifier que Actions est Activé

1. Vérifier la configuration :
   ```bash
   grep -A5 "\[actions\]" /etc/forgejo/app.ini
   ```

2. Sortie attendue :
   ```ini
   [actions]
   ENABLED = true
   DEFAULT_ACTIONS_URL = https://code.forgejo.org
   ```

3. Si manquant, ajouter la section et redémarrer Forgejo

### Enregistrer les Runners

Les runners doivent être enregistrés avant que les workflows puissent s'exécuter :

1. Générer un token d'enregistrement :
   - Naviguer vers **Site Administration** → **Actions** → **Runners**
   - Cliquer sur **"Create registration token"**
   - Copier le token (montré une seule fois)

2. Configuration Puppet attendue (enregistrement automatisé) :
   ```puppet
   forgejo_runner::register { 'runner-1':
     token => '<token_enregistrement>',
     labels => ['ubuntu-latest', 'docker'],
   }
   ```

3. Vérifier que les runners apparaissent dans le panneau d'admin avec statut "idle"

Voir [Configurer les Runners](configurer-runners.md) pour la gestion détaillée des runners.

---

## Activer la Gestion des Dépôts

Les fonctionnalités de dépôt sont au cœur de Forgejo et activées par défaut.

### Configurer les Paramètres des Dépôts

1. Définir les valeurs par défaut des dépôts :
   ```ini
   [repository]
   DEFAULT_BRANCH = main
   DEFAULT_PRIVATE = internal
   ENABLE_PUSH_CREATE_USER = true
   ENABLE_PUSH_CREATE_ORG = true
   DISABLED_REPO_UNITS = repo.ext_wiki,repo.projects
   ```

2. Configurer Git LFS (stockage de gros fichiers) :
   ```ini
   [lfs]
   ENABLED = true
   STORAGE_TYPE = local
   PATH = /var/lib/forgejo/data/lfs
   ```

3. Définir les limites :
   ```ini
   [repository.upload]
   MAX_FILE_SIZE = 100
   
   [repository.pull-request]
   DEFAULT_MERGE_STYLE = merge
   ```

4. Redémarrer Forgejo

### Vérifier les Fonctionnalités de Dépôt

Tester les opérations de dépôt :
```bash
# Créer dépôt de test
curl -X POST "https://forge.entreprise.internal/api/v1/user/repos" \
  -H "Authorization: token <token_admin>" \
  -H "Content-Type: application/json" \
  -d '{"name":"test-repo","private":true}'

# Cloner et tester
git clone https://forge.entreprise.internal/admin/test-repo.git
cd test-repo
echo "Test" > test.txt
git add test.txt
git commit -m "Commit de test"
git push origin main
```

---

## Activer le Registry de Packages (Intégration Nexus)

Dev-Forge s'intègre avec votre instance Nexus existante pour la gestion des packages.

### Configurer le Bridge Registry

**Note** : Ceci crée un proxy/bridge vers Nexus, pas un registry natif Forgejo.

1. Activer le registry de packages :
   ```ini
   [packages]
   ENABLED = true
   
   [packages.proxy]
   TYPE = nexus
   URL = https://nexus.entreprise.internal
   ```

2. Configurer les endpoints de registry par écosystème :
   ```ini
   [packages.npm]
   ENABLED = true
   PROXY_URL = https://nexus.entreprise.internal/repository/npm-group/
   
   [packages.maven]
   ENABLED = true
   PROXY_URL = https://nexus.entreprise.internal/repository/maven-public/
   
   [packages.docker]
   ENABLED = true
   PROXY_URL = https://nexus.entreprise.internal/repository/docker-hosted/
   ```

3. Configurer le passthrough d'authentification :
   ```ini
   [packages.auth]
   NEXUS_TOKEN_URL = https://nexus.entreprise.internal/service/rest/v1/security/user-tokens
   ```

4. Redémarrer Forgejo

### Tester l'Intégration Registry

**Pour npm** :
```bash
npm config set registry https://forge.entreprise.internal/api/packages/npm/
npm login --registry=https://forge.entreprise.internal/api/packages/npm/
npm install express
```

**Pour Maven** :
```xml
<!-- Dans pom.xml -->
<repositories>
  <repository>
    <id>devforge</id>
    <url>https://forge.entreprise.internal/api/packages/maven/</url>
  </repository>
</repositories>
```

**Pour Docker** :
```bash
docker login forge.entreprise.internal
docker pull forge.entreprise.internal/library/alpine:latest
```

---

## Activer le Plugin de Revue de Code

Le plugin de revue de code inclut les merge requests (pull requests) et les workflows d'approbation.

### Configurer les Paramètres de Revue de Code

1. Activer et configurer les merge requests :
   ```ini
   [repository.pull-request]
   WORK_IN_PROGRESS_PREFIXES = WIP:,[WIP],Draft:
   CLOSE_KEYWORDS = close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved
   REOPEN_KEYWORDS = reopen,reopens,reopened
   DEFAULT_MERGE_STYLE = merge
   ENABLE_AUTO_MERGE = true
   ```

2. Configurer les exigences d'approbation :
   ```ini
   [repository.pull-request.branch-protection]
   ENABLE_APPROVALS = true
   REQUIRED_APPROVALS = 1
   DISMISS_STALE_APPROVALS = true
   REQUIRE_SIGNED_COMMITS = false
   ```

3. Configurer les notifications de revue :
   ```ini
   [webhook]
   ALLOWED_HOST_LIST = *
   
   [mailer]
   ENABLED = true
   FROM = forgejo@entreprise.internal
   PROTOCOL = smtp
   SMTP_ADDR = smtp.entreprise.internal
   SMTP_PORT = 587
   ```

4. Redémarrer Forgejo

### Vérifier le Workflow de Revue de Code

Tester le processus de merge request :

1. Créer une branche :
   ```bash
   git checkout -b feature/test-review
   echo "Code de feature" > feature.txt
   git add feature.txt
   git commit -m "Ajout feature"
   git push origin feature/test-review
   ```

2. Ouvrir une merge request dans l'interface web Forgejo :
   - Naviguer vers le dépôt
   - Cliquer sur **"New Pull Request"**
   - Sélectionner `feature/test-review` → `main`
   - Ajouter une description et créer la requête

3. Demander une revue à un membre de l'équipe

4. Vérifier :
   - Le reviewer reçoit une notification
   - Le reviewer peut commenter le code
   - Approbation requise avant le merge
   - Option auto-merge disponible

---

## Activer le Plugin Forgejo Pages

Forgejo Pages permet l'hébergement de sites statiques directement depuis les dépôts Git (équivalent GitHub Pages).

### Configurer Forgejo Pages

1. Activer Pages :
   ```ini
   [pages]
   ENABLED = true
   ROOT_PATH = /var/lib/forgejo/data/pages
   PAGES_URL = https://pages.entreprise.internal/
   ```

2. Configurer les générateurs de sites statiques supportés :
   ```ini
   [pages.generators]
   ENABLE_JEKYLL = true
   ENABLE_HUGO = true
   ENABLE_RAW = true
   ```

3. Redémarrer Forgejo

### Déployer un Site via Pages

1. Créer un fichier de workflow pour build automatique :
   ```yaml
   # .forgejo/workflows/pages.yml
   name: Deploy Pages
   
   on:
     push:
       branches:
         - main
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout
           uses: actions/checkout@v3
         
         - name: Deploy to Pages
           run: |
             # Build du site (Hugo, Jekyll, ou raw HTML)
             echo "Déploiement du site..."
   ```

2. Vérifier le déploiement :
   - Push du code déclenche le workflow
   - Site accessible à `https://pages.entreprise.internal/utilisateur/depot/`

Voir [Référence : Plugins MVP](../reference/plugins-mvp.md) pour configuration détaillée de Pages.

---

## Vérifier la Configuration Complète des Plugins

### Checklist de Vérification Santé

Parcourir cette checklist pour vérifier que tous les plugins MVP sont fonctionnels :

- [ ] **Authentication** : Peut se connecter via LDAP/OIDC
- [ ] **Actions** : Le workflow s'exécute avec succès
- [ ] **Repositories** : Peut créer, cloner, push, pull
- [ ] **Registry** : Peut pull un package via le bridge Nexus
- [ ] **Code Review** : Peut créer et merger une pull request
- [ ] **Pages** : Peut déployer et accéder à un site statique

### Générer un Rapport de Configuration

```bash
# Générer un résumé des plugins actifs
sudo forgejo admin show-config | grep -E "(ENABLED|auth|actions|packages|repository.pull-request|pages)"
```

---

## Dépannage

### L'Authentification Ne Fonctionne Pas

**Problèmes LDAP** :
- Tester le bind LDAP : `ldapsearch -x -H ldap://ldap.entreprise.internal -D "cn=forgejo,ou=services,dc=entreprise,dc=internal" -W -b "ou=users,dc=entreprise,dc=internal"`
- Vérifier que le firewall autorise le port 389 (LDAP) ou 636 (LDAPS)
- Vérifier les identifiants bind dans `app.ini`

**Problèmes OIDC** :
- Vérifier l'URL auto-discovery accessible : `curl https://sso.entreprise.internal/.../.well-known/openid-configuration`
- Vérifier que client ID et secret correspondent à la configuration du fournisseur
- Vérifier l'URI de redirection enregistrée : `https://forge.entreprise.internal/user/oauth2/keycloak/callback`

### Actions Ne Se Déclenche Pas

- Vérifier Actions activé : `grep ENABLED /etc/forgejo/app.ini | grep actions`
- Vérifier runners enregistrés : Web UI → Site Administration → Actions → Runners
- Examiner la livraison webhook : Dépôt → Settings → Webhooks → Recent Deliveries

### Le Registry Retourne 404

- Vérifier que l'instance Nexus est joignable depuis le serveur Forgejo
- Vérifier que la configuration proxy URL correspond aux chemins de dépôt Nexus
- Tester l'accès direct Nexus : `curl -I https://nexus.entreprise.internal/repository/npm-group/`

### Les Approbations de Merge Request Ne Sont Pas Appliquées

- Vérifier que la protection de branche est activée pour la branche cible (généralement `main`)
- Vérifier que `REQUIRED_APPROVALS` est défini correctement
- S'assurer que le reviewer a les permissions appropriées (Write ou Admin)

---

## Prochaines Étapes

- **Personnaliser les workflows** : Adapter la configuration des plugins aux politiques organisationnelles
- **Surveiller l'utilisation** : Suivre l'adoption et les performances des plugins
- **Planifier les extensions** : Identifier des plugins additionnels pour les phases futures

## Documentation Connexe

- [Référence : Plugins MVP](../reference/plugins-mvp.md) — Spécifications détaillées des plugins
- [Explication : Sélection des Plugins (ADR-0004)](../../ADR/0004-plugins-mvp.md) — Justification architecturale
- [Référence : Configuration Forgejo](../reference/configuration-forgejo.md) — Référence de configuration complète

---

## Navigation

🔧 **Autres Guides** : [Configurer Runners](configurer-runners.md) | [Tâches Puppet](taches-puppet.md)  
⬆️ [Retour aux Guides Pratiques](../guide-pratique/)  
📖 [Tutoriels](../tutoriel/) | 📋 [Références](../reference/)
