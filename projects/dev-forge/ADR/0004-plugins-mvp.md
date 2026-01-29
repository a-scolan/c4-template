# ADR-0004 : Sélection des Plugins MVP

## Statut

Accepté

## Contexte

Forgejo offre des fonctionnalités étendues via des features intégrées et plugins optionnels. Le déploiement initial de Dev-Forge doit prioriser les capacités essentielles tout en évitant le bloat de fonctionnalités qui augmente la complexité et la charge de maintenance.

**Principes** :
- **Produit Minimum Viable (MVP)** : Déployer uniquement les fonctionnalités nécessaires pour les workflows de base
- **Release Itérative** : Ajouter des fonctionnalités basées sur les patterns d'utilisation réels, pas la spéculation
- **Simplicité Opérationnelle** : Chaque fonctionnalité ajoute de la complexité de configuration et des modes de défaillance potentiels
- **Capacité de l'Équipe** : Ressources limitées pour le déploiement initial et le support

**Workflow de Développement de Base** (doit supporter) :
1. Authentification des développeurs (intégration identité corporate)
2. Créer/cloner des dépôts Git
3. Pousser du code, déclencher CI/CD automatiquement
4. Tirer des dépendances du package registry
5. Demander une revue de code via merge requests
6. Merger les changements approuvés vers la branche principale

**Déféré pour les Phases Futures** :
- Suivi d'issues et gestion de projet (intégration Jira existante)
- Wiki et documentation (Confluence existant)
- Scanning de sécurité avancé (peut ajouter plus tard)
- Fonctionnalités natives de registry de containers (utilisant intégration Nexus)

### Matrice d'Évaluation des Plugins

| Plugin/Fonctionnalité | Essentiel? | Complexité | Maturité | Décision |
|----------------|-----------|------------|----------|----------|
| **Authentication (LDAP/OIDC)** | ✅ Oui | Faible | Haute | **MVP** |
| **Actions (CI/CD)** | ✅ Oui | Moyenne | Haute | **MVP** |
| **Repositories** | ✅ Oui | Faible | Haute | **MVP** |
| **Registry (bridge Nexus)** | ✅ Oui | Moyenne | Moyenne | **MVP** |
| **Code Review (MR)** | ✅ Oui | Faible | Haute | **MVP** |
| **Pages (hébergement statique)** | ✅ Oui | Faible | Haute | **MVP** |
| Suivi Issues | ❌ Non | Faible | Haute | Phase 2 |
| Tableaux Projets | ❌ Non | Faible | Moyenne | Phase 2 |
| Wiki | ❌ Non | Faible | Haute | Phase 2 |
| Packages (natif) | ❌ Non | Haute | Moyenne | Déféré |
| LFS (Git Large Files) | ⚠️ Peut-être | Faible | Haute | Phase 2 |
| Signature Commit GPG | ⚠️ Peut-être | Faible | Haute | Phase 2 |
| Webhooks | ⚠️ Peut-être | Faible | Haute | Inclus par défaut |
| Auth Externe (GitHub OAuth) | ❌ Non | Faible | Moyenne | Pas nécessaire |

## Décision

Le MVP de Dev-Forge inclura **exactement six plugins essentiels** :

### 1. Plugin d'Authentification (LDAP/OIDC)
**Justification** : L'intégration de l'identité corporate est non-négociable pour un déploiement enterprise.

**Fonctionnalités** :
- Intégration LDAP avec Active Directory
- Intégration OIDC avec provider SSO (Keycloak, etc.)
- Mapping des privilèges admin basé sur les groupes
- Provisioning automatique des utilisateurs à la première connexion

**Pourquoi Essentiel** : Nous ne pouvons pas compter sur les comptes locaux—doit s'intégrer avec la gestion d'identité organisationnelle.

**Complexité** : Faible (bien documenté, stable)

### 2. Plugin Actions (CI/CD)
**Justification** : Les tests automatiques et le building sont au cœur du workflow de développement moderne.

**Fonctionnalités** :
- Syntaxe compatible GitHub Actions
- Exécution de workflow containerisée
- Gestion des secrets
- Déclencheurs manuels et automatisés
- Checks de statut pour les merge requests

**Pourquoi Essentiel** : L'intégration continue est fondamentale/attendue pour toute plateforme Git. Sans CI/CD, Dev-Forge n'est qu'un hôte Git.

**Complexité** : Moyenne (gestion des runners, auto-scaling)

### 3. Plugin Repositories (Hébergement Git)
**Justification** : La fonctionnalité Git de base est la fondation de la plateforme.

**Fonctionnalités** :
- Git clone/push/pull (HTTPS et SSH)
- Gestion des branches et tags
- Règles de protection de branche
- Contrôle d'accès (public/interne/privé)
- Navigateur de fichiers et historique

**Pourquoi Essentiel** : C'est la fonction primaire—tout le reste se construit sur l'hébergement Git.

**Complexité** : Faible (intégré, mature)

### 4. Plugin Registry (Intégration Nexus)
**Justification** : Les développeurs ont besoin d'une gestion de dépendances centralisée.

**Fonctionnalités** :
- Proxy/bridge vers l'instance Nexus existante
- Support npm, Maven, Docker, PyPI, NuGet
- Authentification unifiée (credentials Forgejo → tokens Nexus)
- UI intégrée pour la navigation de packages

**Pourquoi Essentiel** : Le développement moderne nécessite la gestion de packages/dépendances. Utiliser Nexus existant évite l'infrastructure dupliquée tout en fournissant une expérience développeur transparente.

**Complexité** : Moyenne (configuration d'intégration, bridge d'authentification)

### 5. Plugin de Revue de Code (Merge Requests)
**Justification** : La revue de code collaborative est critique pour la qualité du code et le partage de connaissances.

**Fonctionnalités** :
- Workflow de merge request (pull requests)
- Commentaires inline sur le code et discussions
- Exigences d'approbation et gatekeeping
- Intégration avec Actions (checks de statut)
- Capacité d'auto-merge

**Pourquoi Essentiel** : La revue de code est une meilleure pratique pour toute équipe de développement professionnelle. Permet la collaboration et maintient les standards de qualité.

**Complexité** : Faible (intégré, bien développé)

### 6. Plugin Pages (Hébergement de Site Statique)
**Justification** : La documentation et les sites projet sont des besoins communs pour les équipes de développement, permettant l'hébergement en self-service de sites web statiques depuis les dépôts.

**Fonctionnalités** :
- Héberger des sites web statiques directement depuis les branches de dépôt (ex: `gh-pages`, `main/docs/`)
- Déploiement automatique sur push
- Support de domaine personnalisé (via CNAME)
- Chiffrement HTTPS
- Expérience similaire à GitHub Pages

**Pourquoi Essentiel** : Les équipes ont fréquemment besoin d'héberger de la documentation projet, des références API, des démos et des pages de landing. L'hébergement intégré élimine le besoin d'une infrastructure d'hébergement web séparée et fournit un workflow rationalisé (commit → publication).

**Complexité** : Faible (fonctionnalité Forgejo intégrée, configuration minimale)

## Conséquences

### Conséquences Positives

- **Déploiement Focalisé** : Portée claire limite la complexité initiale
- **Temps de Valeur Plus Rapide** : Les développeurs peuvent commencer à utiliser la plateforme immédiatement pour les workflows de base
- **Risque Inférieur** : Moins de pièces mobiles signifie moins de points de défaillance potentiels
- **Critères de Succès Clairs** : Le MVP définit ce que "fonctionnel" signifie
- **Amélioration Itérative** : Peut ajouter des fonctionnalités basées sur la demande réelle
- **Simplicité Opérationnelle** : L'équipe de support a une surface gérable
- **Focus de Formation** : La documentation d'onboarding couvre uniquement l'essentiel

### Conséquences Négatives

- **Ensemble de Fonctionnalités Limité** : Certains développeurs peuvent s'attendre à des fonctionnalités pas dans le MVP (suivi d'issues, wikis)
- **Lacunes d'Intégration** : Doit utiliser des outils externes (Jira) pour certains workflows
- **Risque de Perception** : Les "fonctionnalités manquantes" peuvent créer l'impression d'une plateforme incomplète
- **Complexité Future** : Ajouter des plugins plus tard nécessite planification de migration/mise à jour
- **Développement de Contournements** : Les équipes peuvent construire des solutions personnalisées pour les fonctionnalités manquantes

### Conséquences Neutres

- **Intégration Requise** : Le bridge Nexus nécessite tests et validation
- **Portée de Documentation** : Documenter uniquement les fonctionnalités MVP (simplifie les docs)
- **Charge de Support** : Équipe de support spécialisée sur six fonctionnalités (vs plateforme entière)

## Notes

### Candidats Phase 2

Basé sur les retours MVP, prochains plugins à considérer :

**Haute Priorité** :
- Git LFS (si les équipes travaillent avec de gros fichiers binaires)
- Suivi d'issues (si l'intégration Jira s'avère insuffisante)
- Signature de commit GPG (si la politique de sécurité l'exige)

**Priorité Moyenne** :
- Tableaux de projets/kanban
- Wiki (si docs légères nécessaires)
- Webhooks avancés (intégrations)

**Basse Priorité** :
- Providers d'authentification externes (GitHub OAuth)
- Registry de packages natif (si Nexus devient limitant)
- Scanning de sécurité avancé (SAST/DAST)

### Métriques de Succès

Le MVP est réussi si, après 90 jours :
- 80%+ des développeurs utilisent activement la plateforme pour l'hébergement de code
- 60%+ des projets ont des workflows CI/CD configurés
- 40%+ des merge requests utilisent le workflow de revue de code
- < 5% des tickets de support concernent des fonctionnalités manquantes
- Zéro incident P1/P2 lié aux plugins de base

### Détails d'Implémentation des Plugins

Voir [Référence : Plugins MVP](../docs/reference/plugins-mvp.md) pour la configuration et l'utilisation détaillées.

### Décisions connexes

- [ADR-0001 : Plateforme Forgejo](0001-plateforme-forgejo.md) — La plateforme fournit l'infrastructure de plugin
- [ADR-0002 : Scalabilité Actions](0002-scalabilite-actions.md) — Stratégie de scalabilité du plugin Actions
- [ADR-0007 : Intégration Nexus](0007-integration-nexus.md) — Architecture du plugin Registry

### Références

- Aperçu des Fonctionnalités Forgejo : https://forgejo.org/docs/latest/user/
- Développement Produit MVP : https://en.wikipedia.org/wiki/Minimum_viable_product
- Suivi de demandes de fonctionnalités interne (Confluence : "Demandes de Fonctionnalités Dev-Forge")
