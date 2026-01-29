# ADR-0007 : Intégration du Registry Nexus

## Statut

Accepté

## Contexte

Le développement moderne nécessite une gestion centralisée de packages/dépendances à travers plusieurs écosystèmes (npm, Maven, PyPI, Docker, NuGet). Dev-Forge a besoin d'une solution de package registry qui soit :

**Exigences** :
- Support multi-écosystème (au moins npm, Maven, Docker)
- Déploiement on-premises (exigence organisationnelle)
- Techno-neutre (supporte tous les gestionnaires de packages majeurs)
- Scalable et performant
- Bien intégré avec le workflow de contrôle de source

**Contexte Organisationnel** :
- **Nexus Repository Manager est déjà déployé** et en usage production
- L'équipe infrastructure maintient Nexus pour la gestion de dépendances
- Les développeurs familiers avec les URLs et workflows Nexus
- Configuration Nexus existante (dépôts, proxies, sécurité)
- Investissement dans l'infrastructure et l'expertise Nexus

**Capacités Forgejo** :
- Forgejo inclut un **package registry natif** (fonctionnalité expérimentale/plus récente)
- Supporte npm, Maven, Docker, PyPI, NuGet, et plus
- Authentification intégrée (utilisateurs/tokens Forgejo)
- UI unifiée (packages apparaissent à côté du code)

### Alternatives Considérées

**Registry Natif Forgejo** :
- ✅ Intégration transparente avec dépôts et CI/CD
- ✅ Système d'authentification unique (credentials Forgejo)
- ✅ UI unifiée (code + packages au même endroit)
- ✅ Architecture simplifiée (un service de moins)
- ❌ **Infrastructure dupliquée** (Nexus existe déjà)
- ❌ **Fonctionnalité immature** (plus récente, moins éprouvée en combat)
- ❌ **Charge de migration** (déplacer artifacts existants vers Forgejo)
- ❌ **Expertise perdue** (l'équipe connaît Nexus, pas le registry Forgejo)
- ❌ **Surcharge opérationnelle** (un autre système à sauvegarder, monitorer, scaler)

**JFrog Artifactory** :
- ✅ Riche en fonctionnalités, niveau enterprise
- ✅ Excellent support multi-écosystème
- ✅ Fonctionnalités avancées (build info, promotion d'artifacts)
- ❌ **Licence dispendieuse** (produit commercial)
- ❌ **Nexus déjà déployé** (coût coulé, workflows établis)
- ❌ **Migration requise** depuis Nexus

**Registries Écosystème Auto-Hébergés** (registry npm, serveur PyPI, registry Docker séparément) :
- ✅ Léger, conçu pour un but spécifique
- ✅ Bien documenté pour chaque écosystème
- ❌ **Complexité opérationnelle** (gérer nombreux services)
- ❌ **Expérience inconsistante** (auth, UI, processus différents par écosystème)
- ❌ **Nexus fournit déjà cela** (consolidation via Nexus)

**Registries Package Cloud** (npm, Docker Hub, PyPI.org directement) :
- ✅ Zéro gestion d'infrastructure
- ✅ Haute disponibilité et performance
- ❌ **Viole l'exigence on-premises**
- ❌ **Dépendance aux services externes**
- ❌ **Préoccupations souveraineté des données** (impossible de cacher packages closed-source en interne)
- ❌ **Dépendance Internet sortant**

## Décision

Dev-Forge **s'intégrera avec le Nexus Repository Manager existant** via un pattern proxy/bridge, plutôt que d'utiliser le package registry natif de Forgejo.

### Architecture

**Nexus comme Source de Vérité** :
- Tous les packages stockés dans les dépôts Nexus
- Nexus gère le proxying vers les registries publics (npm, Maven Central, Docker Hub)
- Nexus applique les quotas de stockage et politiques de rétention

**Forgejo comme Passerelle Unifiée** :
- Forgejo fournit un endpoint unifié : `https://forge.company.internal/api/packages/{ecosystem}/`
- Forgejo authentifie les utilisateurs via credentials Forgejo
- Forgejo génère des tokens utilisateur Nexus temporaires
- Requêtes proxyées vers Nexus avec authentification token
- Réponses retournées au client de manière transparente

**Bénéfices** :
- Les développeurs utilisent les credentials Forgejo (pas de login Nexus séparé)
- Les workflows CI/CD utilisent les tokens Forgejo (auth cohérente)
- Packages accessibles via URL de plateforme Git (regroupement logique)
- Nexus reste source de vérité (workflows existants inchangés)

### Pattern d'Intégration

```
Développeur/CI
    ↓
    API Packages Forgejo
    (https://forge.company.internal/api/packages/npm/)
    ↓
    [Authentification : credentials Forgejo]
    ↓
    [Échange Token : Générer token Nexus]
    ↓
    Nexus Repository
    (https://nexus.company.internal/repository/npm-group/)
    ↓
    [Proxy vers registries publics si nécessaire]
    ↓
    Retourner package au client
```

**Flux de Session** :
1. Client s'authentifie vers Forgejo (`npm login`)
2. Forgejo valide les credentials Forgejo
3. Forgejo appelle l'API Nexus : "Générer token utilisateur pour user@company.com"
4. Nexus retourne token temporaire (TTL : 1 heure)
5. Forgejo cache le token (Redis/mémoire)
6. Requêtes subséquentes utilisent token caché jusqu'à expiration
7. Token renouvelé automatiquement à l'expiration

### Configuration

**Forgejo `app.ini`** :
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

**Configuration Nexus** :
- Compte de service Forgejo avec permission génération de token
- Intégration LDAP/OIDC (même provider d'identité que Forgejo)
- Accès API activé pour création de token utilisateur

## Conséquences

### Conséquences Positives

- **Pas d'Infrastructure Dupliquée** : Réutilise l'investissement Nexus existant
- **Stabilité Éprouvée** : Nexus est mature, éprouvé en combat pour la gestion de packages
- **Expérience Développeur Unifiée** : Login Forgejo unique pour code + packages
- **CI/CD Cohérent** : Même token d'authentification pour Git et packages
- **Workflows Existants Préservés** : Les utilisateurs Nexus peuvent continuer l'accès direct
- **Expertise Exploitée** : La connaissance Nexus de l'équipe infrastructure s'applique
- **Stockage Centralisé** : Tous les packages dans un système (Nexus)—simplifie les backups
- **Migration Graduelle** : Peut évaluer le registry natif Forgejo plus tard sans urgence

### Conséquences Négatives

- **Complexité d'Intégration** : Le proxy/bridge ajoute une couche architecturale
- **Latence d'Authentification** : L'échange de token ajoute ~100-200ms par requête initiale
- **Dépendance à Nexus** : Le temps d'arrêt Nexus affecte l'accès packages Dev-Forge
- **UI Forgejo Limitée** : Packages non navigables dans l'interface web Forgejo (doit utiliser UI Nexus)
- **Deux Points de Configuration** : Les changements nécessitent mises à jour dans Forgejo et Nexus
- **Gestion de Token** : Doit surveiller le taux de génération de token et l'efficacité du cache

### Conséquences Neutres

- **Registry Natif Déféré** : Peut revisiter la décision si le registry Forgejo mûrit significativement
- **Monitoring Nexus** : Doit assurer que Nexus est scale appropriément pour la charge accrue
- **Option de Fallback** : Les URLs Nexus directes restent disponibles comme fallback

## Notes

### Structure Dépôt Nexus

**Setup Recommandé** :
- **Dépôts hébergés** : Packages internes (publiés par les développeurs)
- **Dépôts proxy** : Cacher les registries publics (npm, Maven Central)
- **Dépôts groupe** : Combiner hébergé + proxy (endpoint unique)

**Exemple** :
- `npm-hosted` : Packages npm internes de l'entreprise
- `npm-proxy` : Cache npmjs.org
- `npm-group` : Combine hébergé + proxy → Forgejo pointe ici

### Chemin de Migration vers Registry Natif (Futur)

Si le registry natif Forgejo devient convaincant :

1. **Phase d'Évaluation** : Tester registry Forgejo en staging avec sous-ensemble de packages
2. **Opération Duale** : Exécuter Nexus et registry Forgejo (migration graduelle)
3. **Migration** : Syncer packages de Nexus vers Forgejo
4. **Cutover** : Mettre à jour CI/CD pour utiliser endpoints Forgejo natifs
5. **Décommissionnement** : Éliminer progressivement la dépendance Nexus

**Critères de Décision pour Migration** :
- Parité fonctionnalités registry Forgejo avec Nexus (maturité)
- Disponibilité outillage de migration
- Aucune disruption opérationnelle
- Bénéfices clairs vs intégration (performance, fonctionnalités, coût)

### Considérations Sécurité

**Sécurité Token** :
- Tokens cachés en mémoire/Redis (non persistés sur disque)
- Tokens expirent automatiquement (TTL 1 heure)
- Forgejo log la génération token pour audit

**Sécurité Réseau** :
- Communication Forgejo ↔ Nexus via HTTPS
- Nexus pas directement accessible depuis Internet (derrière firewall)
- Authentification API Nexus via compte service (moindre privilège)

### Optimisation Performance

**Stratégie Caching** :
- Caching token réduit appels API Nexus (améliore latence)
- Forgejo ne cache PAS les données packages (Nexus gère cela)
- Headers caching HTTP passés de manière transparente

**Métriques Monitoring** :
- Taux hit cache token (cible : > 90%)
- Latence échange token (cible : < 200ms p95)
- Taux requête Nexus depuis Forgejo
- Débit téléchargement packages

### Décisions Connexes

- [ADR-0004 : Plugins MVP](0004-plugins-mvp.md) — Plugin registry fait partie du MVP
- [ADR-0006 : Neutralité Technologique](0006-neutralite-technologique.md) — Nexus supporte tous les écosystèmes
- [ADR-0001 : Plateforme Forgejo](0001-plateforme-forgejo.md) — Forgejo comme interface développeur primaire

### Références

- Documentation Nexus Repository Manager : https://help.sonatype.com/repomanager3
- API REST Nexus : https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api
- API User Token Nexus : https://help.sonatype.com/repomanager3/integrations/rest-and-integration-api/user-account-api
- Documentation Nexus interne (Confluence : "Infrastructure/Nexus")
