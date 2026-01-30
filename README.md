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

## 📚 Documentation

### Pour Démarrer

**Nouveau sur Dev-Forge ?** Commencez ici :
- [Intégration Développeur](projects/dev-forge/docs/tutoriel/01-integration-developpeur.md) — Créer votre premier dépôt
- [Premier Pipeline](projects/dev-forge/docs/tutoriel/02-premier-pipeline.md) — Configurer CI/CD avec Forgejo Actions

### Guides de Configuration

**Besoin de configurer quelque chose ?** Consultez les guides pratiques :
- [Configurer les Runners](projects/dev-forge/docs/guide-pratique/configurer-runners.md) — Mise à l'échelle et configuration
- [Configurer les Plugins](projects/dev-forge/docs/guide-pratique/configurer-plugins.md) — Activer les fonctionnalités MVP
- [Tâches Puppet](projects/dev-forge/docs/guide-pratique/taches-puppet.md) — Automatisation des déploiements

### Références Techniques

**Besoin de spécifications détaillées ?**
- [Plugins MVP](projects/dev-forge/docs/reference/plugins-mvp.md) — Auth, Actions, Repos, Registry, Code Review, Pages
- [Configuration Forgejo](projects/dev-forge/docs/reference/configuration-forgejo.md) — Paramètres système

### Comprendre les Décisions

**Pourquoi cette architecture ?** Consultez les [Architecture Decision Records (ADRs)](projects/dev-forge/ADR/) :
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

## 🤝 Trouver ce dont vous avez besoin

- **Questions d'architecture ?** → [ADRs](projects/dev-forge/ADR/)
- **Comment faire X ?** → [Guides Pratiques](projects/dev-forge/docs/guide-pratique/)
- **Débuter avec la plateforme ?** → [Tutoriels](projects/dev-forge/docs/tutoriel/)
- **Spécifications techniques ?** → [Référence](projects/dev-forge/docs/reference/)

---

<details>
<summary>💡 À propos de l'organisation de cette documentation</summary>

Cette documentation suit le framework [Diataxis](https://diataxis.fr/), qui organise le contenu selon 4 besoins utilisateurs :
- **Tutoriels** : Apprendre en faisant (orientation apprentissage)
- **Guides pratiques** : Accomplir des tâches spécifiques (orientation résolution de problèmes)
- **Référence** : Consulter des spécifications techniques (orientation information)
- **Explication** : Comprendre les concepts et décisions (orientation compréhension)

Cette structure aide à trouver rapidement le bon type d'information selon votre besoin.
</details>

---

**Note** : Cette architecture est vivante. Au fur et à mesure que la plateforme évolue, la documentation et les modèles seront mis à jour pour refléter les décisions de conception actuelles et les détails d'implémentation.