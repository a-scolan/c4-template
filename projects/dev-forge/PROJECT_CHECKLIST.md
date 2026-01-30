# Checklist du Projet Dev-Forge

## Phase 1: Documentation Utilisateur 🔄 EN COURS (80%)

- [x] README.md racine avec navigation claire
- [ ] **Tutoriels** (2 fichiers - 1 à mettre à jour)
  - [ ] `01-onboarding-developer.md` - ⚠️ À METTRE À JOUR : Ajouter section configuration SSH
    - [ ] Générer une paire de clés SSH (ssh-keygen)
    - [ ] Ajouter la clé publique dans Forgejo (Settings > SSH Keys)
    - [ ] Tester la connexion SSH (`ssh -T git@forgejo.example.com`)
    - [ ] Cloner les dépôts via SSH (git@forgejo.example.com:org/repo.git)
  - [x] `02-first-pipeline.md` - Configuration du premier pipeline CI/CD
- [ ] **Guides pratiques** (4 fichiers - 1 manquant)
  - [x] `configure-runners.md` - Configuration de l'auto-scaling des runners
  - [x] `setup-plugins.md` - Activation des plugins MVP
  - [x] `puppet-tasks.md` - Attentes pour les tâches de déploiement
  - [ ] `forgejo-web-ui.md` - ❌ NOUVEAU : Guide interface web pour chefs de projet / profils non techniques
    - [ ] Navigation dans l'interface Forgejo
    - [ ] Créer et gérer des projets/organisations
    - [ ] Gérer les membres et permissions
    - [ ] Suivre l'activité des dépôts
    - [ ] Visualiser les pipelines CI/CD
    - [ ] Consulter les pages statiques (Forgejo Pages)
    - [ ] ⚠️ Nécessite validation sur environnement web réel
- [x] **Références** (2 fichiers)
  - [x] `plugins-mvp.md` - Référence technique des 6 plugins MVP (incluant Forgejo Pages)
  - [x] `forgejo-config.md` - Configuration système Forgejo
- [x] **Explications**
  - [x] `explanation/README.md` - Pointeur vers les ADR

## Phase 2: Architecture Decision Records 🔄 EN COURS (87%)

- [x] ADR-0001: Sélection de la plateforme Forgejo
  - [x] Analyse détaillée des alternatives (GitLab, Gitea, GitHub Enterprise, BitBucket)
  - [x] **Justification critique de rejet de GitLab** : procédures de maintenance complexes
  - [x] Documentation des conséquences
- [x] ADR-0002: Stratégie de scalabilité des Actions
  - [x] Configuration staging: **2 runners de base**, scale-down **5 minutes**
  - [x] **Clarification du rôle du staging** : validation fonctionnelle SEULEMENT
  - [x] Production capacity sizing strategy
- [x] ADR-0003: Automatisation Puppet
- [x] ADR-0004: Plugins MVP (**6 plugins incluant Forgejo Pages**)
- [x] ADR-0005: Zones réseau
- [x] ADR-0006: Neutralité technologique
- [x] ADR-0007: Intégration Nexus
- [ ] ADR-0008: Politique SSH obligatoire pour Git ❌ NOUVEAU
  - [ ] **Décision** : TOUS les accès Git doivent utiliser SSH (jamais HTTPS)
  - [ ] **Contexte** : Sécurité, gestion centralisée des clés, traçabilité
  - [ ] **Conséquences** : Configuration SSH obligatoire pour tous les développeurs
  - [ ] **Alternatives rejetées** : HTTPS avec tokens (moins sécurisé, gestion distribuée)

## Phase 3: System Design & Modélisation Architecture C4 ❌ NON COMMENCÉ (0%)

### 3.1 Planification System Design (REQUIS AVANT MODÉLISATION)
- [ ] **Clarifier le périmètre fonctionnel de chaque système**
  - [ ] Définir les responsabilités précises de `devforge` (quelles fonctionnalités?)
  - [ ] Définir les responsabilités de `nexus` (rôle exact dans l'écosystème)
  - [ ] Définir les responsabilités de `ldapServer` (authentification uniquement? gestion groupes?)
  - [ ] Définir les responsabilités de `puppetForge` (modules communautaires uniquement?)
  - [ ] Définir les responsabilités de `publicRepos` (quels repos? GitHub, GitLab, autres?)
- [ ] **Documenter les capacités de chaque container**
  - [ ] `forgejoWeb`: Quelles fonctionnalités expose l'interface web?
  - [ ] `gitBackend`: Quelles opérations Git supportées?
  - [ ] `actionsScheduler`: Algorithme de scheduling, priorités?
  - [ ] `runnerPool`: Gestion lifecycle, health checks?
  - [ ] `postgresDb`: Schémas, tables principales, stratégie backup?
  - [ ] `puppetMaster`: Configuration management, catalogues?
  - [ ] `puppetAgents`: Fréquence de sync, modes d'exécution?
- [ ] **Identifier les cas d'usage critiques**
  - [ ] Quels workflows métier doivent être documentés?
  - [ ] Quelles interactions utilisateur sont prioritaires?
  - [ ] Quels scénarios de performance/scalabilité tester?

### 3.2 Modèle Système (EN ATTENTE DE PLANIFICATION)
- [ ] system-model.c4
  - [ ] C1 Acteurs (developer, admin, ciSystem)
  - [ ] C1 Systèmes (devforge, nexus, ldapServer, puppetForge, publicRepos)
  - [ ] C2 Containers (forgejoWeb, gitBackend, actionsScheduler, runnerPool, postgresDb, puppetMaster, puppetAgents)
  - [ ] C3 Components (authModule, repoModule, actionsModule, registryBridge, codeReviewModule, pagesModule)
  - [ ] Relations entre éléments (C1/C2/C3)

### 3.3 Vues Système (EN ATTENTE DU MODÈLE)
- [ ] system-views.c4
  - [ ] C1: Vue contexte système
  - [ ] C2: Vues containers (focus CI/CD, automation)
  - [ ] C3: Vues composants (plugins MVP)
  - [ ] Vues dynamiques: cas d'usage identifiés en phase de planification

### 3.4 Modèle Déploiement (EN ATTENTE DES VUES SYSTÈME)
- [ ] deployment-staging.c4
  - [ ] Topologie infrastructure environnement staging
  - [ ] Zones réseau (DMZ, AppTier, DataTier, InfraZone)
  - [ ] Spécifications VM avec tableaux markdown
  - [ ] Relations instanceOf
- [ ] deployment-views.c4
  - [ ] Vues topologie réseau
  - [ ] Vues placement VM

## Phase 4: Validation ⏳ EN ATTENTE

- [ ] Utiliser le skill test-model pour valider system-model.c4
- [ ] Prévisualiser les vues avec mcp_likec4_open-view
  - [ ] c1_context
  - [ ] c2_cicd_focus
  - [ ] c3_mvp_plugins
  - [ ] usecase_cicd_workflow
- [ ] Vérifier que toutes les références d'éléments se résolvent
- [ ] Vérifier la cohérence des relations

## Phase 5: Extension Production ⏳ EN ATTENTE

- [ ] Créer deployment-production.c4
- [ ] Spécifications environnement production (scaled from staging)
- [ ] Mises à jour ADR pour production
- [ ] Documentation spécifique production

## Phase 6: Diagrammes de Workflow (Mermaid) ⏳ EN ATTENTE

- [ ] Flux d'onboarding développeur (support tutoriels)
- [ ] Workflow pipeline CI/CD (push → completion)
- [ ] Processus de code review (lifecycle MR)
- [ ] Comportement d'auto-scaling des runners
- [ ] Flux de déploiement Puppet
- [ ] Flux d'authentification (LDAP/OIDC)

## Prochaines Étapes IMMÉDIATES

### Priorité Haute (Compléter Phases 1 & 2)

1. **📝 PHASE 2: ADR-0008 - Politique SSH** (RAPIDE)
   - Créer ADR-0008 documentant la décision SSH obligatoire
   - Justifier le rejet de HTTPS (sécurité, gestion centralisée)
   - Documenter les implications pour les développeurs

2. **📚 PHASE 1: Mise à jour tutoriel développeur** (MOYEN)
   - Mettre à jour `01-onboarding-developer.md` avec section SSH complète
   - Étapes : génération clés, ajout dans Forgejo, test connexion
   - Exemples de commandes SSH pour clone/push/pull

3. **🖥️ PHASE 1: Nouveau guide interface web** (LONG - NÉCESSITE VALIDATION WEB)
   - Créer `forgejo-web-ui.md` pour profils non techniques
   - Navigation, gestion projets, permissions, suivi activité
   - ⚠️ Requiert accès à environnement Forgejo pour screenshots/validation

### Priorité Normale (Phase 3)

4. **📋 PHASE 3.1: Planification System Design**
   - Clarifier les responsabilités fonctionnelles de chaque système
   - Documenter les capacités de chaque container
   - Identifier les cas d'usage critiques à modéliser
   - **Output attendu**: Document de design système (markdown ou ADR)

5. **🏗️ PHASE 3.2: Modélisation** (après planification)
   - Créer system-model.c4 avec définitions claires
   - Créer system-views.c4 basé sur cas d'usage identifiés

6. **🏛️ PHASE 3.4: Déploiement** (après modèle système)
   - Créer deployment-staging.c4
   - Créer deployment-views.c4

7. **✅ PHASE 4: Validation** (après modèle complet)
   - Valider avec skill test-model
   - Prévisualiser vues avec mcp_likec4_open-view

## Leçons Apprises & Skills Disponibles

**Skills LikeC4 améliorés** (disponibles pour utilisation future):
- **create-relationship**: Syntaxe correcte `-[kind]->` documentée avec anti-patterns
- **create-sequence-view**: Interdiction parent-child dans vues dynamiques
- **troubleshoot-errors**: Erreurs courantes (syntax, parent-child, rank same)

## Résumé de Progression

- **Phase 1**: 🔄 80% (8/10 fichiers - 1 guide manquant + 1 tutoriel à mettre à jour)
- **Phase 2**: 🔄 87% (7/8 ADRs - ADR-0008 SSH à créer)
- **Phase 3**: ❌ 0% (RÉINITALISÉ - planification system design requise avant modélisation)
- **Phase 4**: ⏳ 0% (en attente Phase 3)
- **Phase 5**: ⏳ 0% (en attente Phase 4)
- **Phase 6**: ⏳ 0% (en attente Phase 5)

**Progression Globale**: ~28% (1.67/6 phases terminées)

### Fichiers Documentation à Compléter
- ⚠️ `tutoriel/01-onboarding-developer.md` : Ajouter section configuration SSH (génération clés, ajout dans Forgejo, test connexion)
- ❌ `guide-pratique/forgejo-web-ui.md` : Nouveau guide pour profils non techniques / chefs de projet

### Détails Phase 3
- ❌ **3.1 Planification System Design**: Non commencé (PRIORITÉ)
- ❌ **3.2 system-model.c4**: Non commencé (bloqué par 3.1)
- ❌ **3.3 system-views.c4**: Non commencé (bloqué par 3.2)
- ❌ **3.4 deployment-staging.c4**: Non commencé (bloqué par 3.3)
- ❌ **3.4 deployment-views.c4**: Non commencé (bloqué par 3.3)

### Raison de la Réinitialisation
Besoin de clarifier le périmètre fonctionnel de chaque système et les capacités de chaque container AVANT de modéliser. Une planification system design solide évitera les ambiguïtés et garantira un modèle C4 cohérent.

## Notes Importantes

### 🔐 Politique SSH Obligatoire (SANS EXCEPTION)

**RÈGLE ABSOLUE** : Tous les accès Git à Dev-Forge DOIVENT utiliser SSH, jamais HTTPS.

**Raisons** :
- 🔒 **Sécurité renforcée** : Clés SSH plus robustes que passwords/tokens HTTPS
- 🏢 **Gestion centralisée** : Clés publiques gérées dans Forgejo, révocation immédiate
- 📊 **Traçabilité** : Chaque clé SSH identifie uniquement un utilisateur
- 🚫 **Pas de credentials en clair** : Aucun token/password stocké localement

**Implications pour les développeurs** :
- ✅ Génération obligatoire de clés SSH (ssh-keygen)
- ✅ Ajout de la clé publique dans Forgejo (Settings > SSH Keys)
- ✅ Utilisation exclusive de URLs SSH : `git@forgejo.example.com:org/repo.git`
- ❌ URLs HTTPS désactivées : `https://forgejo.example.com/org/repo.git` (non supporté)

**Documentation** : Voir tutoriel `01-onboarding-developer.md` (section SSH à ajouter) et ADR-0008 (à créer)

### ⚠️ Rôle de l'Environnement Staging

**IMPORTANT** : Le staging sert **exclusivement** à la **validation fonctionnelle** de la plateforme Dev-Forge :

**Ce que le staging valide** :
- ✅ Le provisioning et l'auto-scaling des runners fonctionnent correctement
- ✅ Les workflows s'exécutent avec succès avec authentification appropriée
- ✅ Le stockage et la récupération des artifacts fonctionnent
- ✅ L'intégration avec l'interface web Forgejo est fluide
- ✅ L'automatisation Puppet gère correctement le cycle de vie des runners
- ✅ La connectivité réseau et les règles firewall sont correctes
- ✅ Les fichiers de configuration et variables sont correctement templat-és

**Ce que le staging ne fait PAS** :
- ❌ Tests de performance ou benchmarking
- ❌ Évaluation de la capacité production
- ❌ Tests de charge (synthétiques ou réels)
- ❌ Simulation de charge de travail production
- ❌ Évaluation des limites de scalabilité

**Pourquoi** : Le staging est délibérément minimal (2 runners de base, max 10) pour minimiser les coûts d'infrastructure. Les métriques de performance et le dimensionnement production DOIVENT être validés en utilisation réelle avec les charges de travail réelles des projets sur les 30-60 premiers jours.

### Plugins MVP (6 plugins)

1. **Authentication** - Intégration LDAP/OIDC SSO avec mapping groupes/permissions
2. **Actions** - CI/CD Forgejo Actions avec auto-scaling runners
3. **Repositories** - Gestion complète des dépôts Git (branches, protection, accès)
4. **Registry Bridge** - Proxy Nexus pour packages (npm, Maven, Docker, PyPI)
5. **Code Review** - Merge requests avec commentaires inline, approbations, status checks
6. **Forgejo Pages** - Hébergement de sites statiques (équivalent GitHub Pages)

### Configuration Staging

- **Runners de base** : 2 (validation fonctionnelle uniquement)
- **Runners max** : 10
- **Délai scale-down** : 5 minutes
- **Seuil scale-up** : 2 workflows en attente
- **Objectif** : Prouver que le déploiement fonctionne correctement, PAS évaluer les performances

### Configuration Production (Prévue)

- **Runners de base** : 8 (estimation initiale conservative, **à ajuster**)
- **Runners max** : 25
- **Délai scale-down** : 5 minutes
- **Monitoring** : Ajustement mensuel basé sur métriques réelles (profondeur queue, temps d'attente, utilisation)
- **Objectif** : Mesures en conditions réelles sur 30-60 jours pour tuning optimal

## Références

- ADR-0001: Sélection plateforme Forgejo (justification rejet GitLab)
- ADR-0002: Stratégie scalabilité Actions (staging = validation fonctionnelle)
- ADR-0004: Plugins MVP (6 plugins incluant Forgejo Pages)
- Documentation Forgejo Pages: https://forgejo.org/docs/next/user/packages/pages/

- **Documentation**: 🔄 80% (8/10 files - 1 guide + 1 màj manquants)
- **ADRs**: 🔄 87% (7/8 decisions - ADR-0008 SSH manquant)
- **System Design**: ❌ 0% (planning required)
- **System Model**: ❌ 0% (blocked by system design)
- **Deployment Model**: ❌ 0% (blocked by system model)
- **Validation**: ⏳ 0% (pending models)
- **Production**: ⏳ 0% (pending staging validation)

**Overall Project Progress**: ~28%

**NEXT ACTION**: Compléter Phases 1 & 2 (ADR-0008 SSH + tutoriel SSH + guide interface web)
