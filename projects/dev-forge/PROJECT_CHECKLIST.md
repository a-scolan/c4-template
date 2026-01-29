# Checklist du Projet Dev-Forge

## Phase 1: Structure de Documentation (Diataxis) ✅ TERMINÉ

- [x] README.md racine avec navigation Diataxis
- [x] **Tutoriels** (2 fichiers)
  - [x] `01-onboarding-developer.md` - Premier dépôt pour un nouveau développeur
  - [x] `02-first-pipeline.md` - Configuration du premier pipeline CI/CD
- [x] **Guides pratiques** (3 fichiers)
  - [x] `configure-runners.md` - Configuration de l'auto-scaling des runners
  - [x] `setup-plugins.md` - Activation des plugins MVP
  - [x] `puppet-tasks.md` - Attentes pour les tâches de déploiement
- [x] **Références** (2 fichiers)
  - [x] `plugins-mvp.md` - Référence technique des 6 plugins MVP (incluant Forgejo Pages)
  - [x] `forgejo-config.md` - Configuration système Forgejo
- [x] **Explications**
  - [x] `explanation/README.md` - Pointeur vers les ADR

## Phase 2: Architecture Decision Records ✅ TERMINÉ

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

## Phase 3: Modélisation Architecture C4 ⏸️ EN PAUSE

### Modèle Système
- [x] C1 Acteurs (developer, admin, ciSystem)
- [x] C1 Systèmes (devforge, nexus, ldapServer, puppetForge, publicRepos)
- [x] C2 Containers (forgejoWeb, gitBackend, actionsScheduler, runnerPool, postgresDb, puppetMaster, puppetAgents)
- [x] **C3 Components** (authModule, repoModule, actionsModule, registryBridge, codeReviewModule, **pagesModule**)
- [x] Toutes les relations définies (niveaux C1/C2/C3)
- [x] Tags corrigés (placement après l'accolade ouvrante)

### Vues Système
- [ ] ⏸️ EN PAUSE: system-views.c4
  - Statut: Fichier créé avec erreurs de syntaxe
  - Problème bloquant: Syntaxe LikeC4 pour composants imbriqués pas claire

### Modèle Déploiement
- [ ] ❌ NON COMMENCÉ: deployment-staging.c4
  - Topologie infrastructure environnement staging
  - Zones réseau (DMZ, AppTier, DataTier, InfraZone)
  - Spécifications VM avec tableaux markdown
  - Relations instanceOf

### Modèle Code
- [ ] ❌ NON COMMENCÉ: system-code.c4 (priorité basse)

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

## Obstacles Actuels

1. **Références Composants LikeC4** : Besoin de résoudre la syntaxe pour accéder aux composants imbriqués dans les containers depuis les vues
2. **Références Systèmes Externes** : Confirmer pourquoi les systèmes externes définis dans system-model.c4 ne se résolvent pas dans system-views.c4

## Prochaines Étapes (Lors de la Reprise du Travail C4)

1. Rechercher la documentation LikeC4 pour les patterns d'accès aux composants imbriqués
2. Corriger la syntaxe des références de composants dans system-views.c4
3. Valider le modèle avec le skill test-model
4. Prévisualiser les vues clés pour assurer le rendu correct
5. Créer deployment-staging.c4

## Résumé de Progression

- **Phase 1**: 100% (8/8 fichiers de documentation créés)
- **Phase 2**: 100% (7/7 ADRs créés et mis à jour)
- **Phase 3**: 50% (system-model.c4 terminé, system-views.c4 en pause)
- **Phase 4**: 0% (en attente Phase 3)
- **Phase 5**: 0% (en attente Phase 4)
- **Phase 6**: 0% (en attente)

**Progression Globale**: ~40% (2.5/6 phases terminées)

## Notes Importantes

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

- **Documentation**: 100% (8/8 files)
- **ADRs**: 100% (7/7 decisions)
- **System Model**: 90% (model complete, views paused)
- **Deployment Model**: 0% (not started)
- **Validation**: 0% (pending model completion)
- **Production**: 0% (pending staging validation)

**Overall Project Progress**: ~45%
