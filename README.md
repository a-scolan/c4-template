# Dev-Forge : Plateforme de Développement Moderne

**Une plateforme de développement on-premises, techno-agnostique, propulsée par Forgejo et Puppet**

Dev-Forge fournit aux équipes de développement une plateforme Git complète auto-hébergée incluant automation CI/CD, revue de code, gestion de packages, et provisioning d'infrastructure automatisé—tout en restant neutre face aux langages de programmation et frameworks que les équipes choisissent d'utiliser.

## 🎯 Présentation du Projet

**Statut** : Phase de Planification & Documentation Initiale  
**Environnement Cible** : Infrastructure on-premises  
**Déploiement Initial** : Environnement staging avec runners Forgejo Actions scalables  
**Futur** : Environnement production suivant l'architecture staging validée

### Technologies Clés

- **Forgejo** : Hébergement Git, CI/CD (Actions), revue de code, intégration registry de packages
- **Puppet** : Automatisation d'infrastructure et gestion de configuration
- **Nexus** : Registry externe de packages (intégration existante)
- **PostgreSQL** : Backend base de données Forgejo

## 📚 Structure de Documentation (Framework Diataxis)

Ce projet suit le framework de documentation [Diataxis](https://diataxis.fr/), organisant le contenu selon les besoins utilisateurs :

### 📖 [Tutoriels](projects/dev-forge/docs/tutoriel/) — Apprendre en Faisant
*Pour les développeurs nouveaux sur la plateforme*

- [01 - Intégration Développeur](projects/dev-forge/docs/tutoriel/01-integration-developpeur.md) — Créer votre premier dépôt
- [02 - Premier Pipeline](projects/dev-forge/docs/tutoriel/02-premier-pipeline.md) — Configurer CI/CD avec Forgejo Actions

### 🔧 [Guides Pratiques](projects/dev-forge/docs/guide-pratique/) — Tâches Pratiques
*Pour les praticiens accomplissant des objectifs spécifiques*

- [Configurer les Runners](projects/dev-forge/docs/guide-pratique/configurer-runners.md) — Mettre à l'échelle et configurer les runners Forgejo Actions
- [Configurer les Plugins](projects/dev-forge/docs/guide-pratique/configurer-plugins.md) — Activer et configurer les plugins MVP
- [Tâches Puppet](projects/dev-forge/docs/guide-pratique/taches-puppet.md) — Résultats attendus pour les tâches de déploiement

### 📋 [Référence](projects/dev-forge/docs/reference/) — Faits Techniques
*Pour les praticiens nécessitant spécifications et détails*

- [Plugins MVP](projects/dev-forge/docs/reference/plugins-mvp.md) — Auth, Actions, Repos, Registry, Code Review, Pages
- [Configuration Forgejo](projects/dev-forge/docs/reference/configuration-forgejo.md) — Référence de configuration système

### 💡 [Explication](projects/dev-forge/ADR/) — Comprendre les Décisions
*Pour comprendre le "pourquoi" derrière les choix architecturaux*

Voir [Architecture Decision Records (ADRs)](projects/dev-forge/ADR/) pour la justification détaillée :
- ADR-0001 : Sélection de la Plateforme Forgejo
- ADR-0002 : Stratégie de Scalabilité Actions
- ADR-0003 : Automatisation Puppet
- ADR-0004 : Sélection des Plugins MVP
- ADR-0005 : Architecture des Zones Réseau
- ADR-0006 : Neutralité Technologique
- ADR-0007 : Intégration Registry Nexus

## 🏗️ Architecture & Modèles

### Modèles d'Architecture C4 (LikeC4)

Architecture système complète modélisée à tous les niveaux C4 :

- **[Modèle Système](projects/dev-forge/system-model.c4)** — Éléments, containers et composants
- **[Vues Système](projects/dev-forge/system-views.c4)** — Diagrammes de contexte, container et composants
- **[Déploiement (Staging)](projects/dev-forge/deployment-staging.c4)** — Topologie d'infrastructure et environnement runtime

**Prévisualiser les Modèles** : Utiliser le serveur MCP LikeC4 ou l'extension VS Code pour visualiser les diagrammes

### Diagrammes de Workflow (Mermaid)

*À venir en Phase 6* : Workflows visuels pour tâches courantes
- Flow d'intégration développeur
- Déclenchement et exécution CI/CD
- Comportement d'auto-scaling des runners
- Orchestration de déploiement Puppet

## 🚀 Progression du Projet

Voir [PROJECT_CHECKLIST.md](projects/dev-forge/PROJECT_CHECKLIST.md) pour le suivi détaillé des phases :

- ✅ **Phase 1** : Structure de Documentation (Diataxis)
- ✅ **Phase 2** : Architecture Decision Records
- 🔄 **Phase 3** : Modélisation d'Architecture C4
- ⏳ **Phase 4** : Validation & Prévisualisation des Modèles
- ⏳ **Phase 5** : Extension Environnement Production
- ⏳ **Phase 6** : Diagrammes de Workflow (Mermaid)

## 💎 Principes Clés

1. **Techno-Agnostique** : La plateforme supporte tout langage de programmation ou framework
2. **CI/CD Scalable** : Runners Forgejo Actions containerisés avec auto-scaling
3. **On-Premises First** : Contrôle complet sur infrastructure et données
4. **Opérations Automatisées** : Provisioning et configuration pilotés par Puppet
5. **Conception Modulaire** : Approche plugin MVP assure une plateforme focalisée et maintenable

## 🤝 Contribuer

Questions d'architecture ? Commencez par les [ADRs](projects/dev-forge/ADR/)  
Questions d'implémentation ? Consultez les [Guides Pratiques](projects/dev-forge/docs/guide-pratique/)  
Besoin de comprendre quelque chose ? Lisez les [Explications](projects/dev-forge/ADR/)  
Prêt à apprendre ? Suivez les [Tutoriels](projects/dev-forge/docs/tutoriel/)

---

**Note** : Cette architecture est vivante. Au fur et à mesure que la plateforme évolue, la documentation et les modèles seront mis à jour pour refléter les décisions de conception actuelles et les détails d'implémentation.

