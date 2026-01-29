# Explication : Dossiers de Décision d'Architecture

Ce répertoire contient les Architecture Decision Records (ADRs) documentant les décisions significatives prises lors de la conception et de la mise en œuvre de la plateforme Dev-Forge.

---

## Qu'est-ce qu'un ADR ?

Les Architecture Decision Records capturent le **pourquoi** derrière les choix architecturaux. Ils documentent :
- Le contexte et les forces qui ont conduit à une décision
- La décision elle-même et sa justification
- Les conséquences (positives, négatives et neutres) de ce choix

---

## Index des ADRs

### Sélection de Plateforme & Technologie

- **[ADR-0001: Sélection de la Plateforme Forgejo](../../ADR/0001-plateforme-forgejo.md)**  
  Pourquoi nous avons choisi Forgejo plutôt que GitLab, Gitea et d'autres plateformes d'hébergement Git

- **[ADR-0003: Puppet pour l'Automatisation d'Infrastructure](../../ADR/0003-automatisation-puppet.md)**  
  Pourquoi nous avons sélectionné Puppet pour la gestion de configuration et l'orchestration de déploiement

- **[ADR-0007: Intégration du Registry Nexus](../../ADR/0007-integration-nexus.md)**  
  Pourquoi nous intégrons avec Nexus existant au lieu d'utiliser le registry natif de Forgejo

### Scalabilité & Architecture

- **[ADR-0002: Stratégie de Scalabilité Actions](../../ADR/0002-scalabilite-actions.md)**  
  Architecture du pool de runners et conception d'auto-scaling pour les charges de travail CI/CD

- **[ADR-0005: Architecture des Zones Réseau](../../ADR/0005-zones-reseau.md)**  
  Stratégie de segmentation réseau (DMZ, AppTier, DataTier) et frontières de sécurité

### Fonctionnalités

- **[ADR-0004: Sélection des Plugins MVP](../../ADR/0004-plugins-mvp.md)**  
  Six plugins essentiels pour le déploiement initial (auth, actions, repos, registry, code review, pages)

- **[ADR-0006: Principe de Neutralité Technologique](../../ADR/0006-neutralite-technologique.md)**  
  Conception de la plateforme pour supporter tout langage de programmation ou framework

---

## Cycle de Vie des ADRs

Les ADRs suivent ces statuts :

- **Proposed**: En cours de considération et discussion
- **Accepted**: Décision prise et en cours d'implémentation
- **Deprecated**: N'est plus recommandé mais pas encore remplacé
- **Superseded**: Remplacé par un ADR plus récent (référence incluse)

Chaque ADR inclut son statut actuel en haut du document.

---

## Quand Créer un ADR

Créez un ADR lors de décisions concernant :
- ✅ Sélection de technologie (bases de données, frameworks, plateformes)
- ✅ Patterns architecturaux (microservices, event-driven, etc.)
- ✅ Conception d'infrastructure (topologie réseau, stratégies de scaling)
- ✅ Approches de sécurité et conformité
- ✅ Patterns d'intégration avec systèmes externes

Ne créez **pas** d'ADRs pour :
- ❌ Détails d'implémentation (ceux-ci vont dans les commentaires de code ou guides pratiques)
- ❌ Contournements temporaires
- ❌ Changements de configuration routiniers
- ❌ Corrections de bugs

---

## Template ADR

Les nouveaux ADRs doivent suivre la [structure du template](../template/ADR/0000-template.md) :

```markdown
# ADR-NNNN: Titre

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
[Pourquoi cette décision est-elle nécessaire ? Quelles forces sont en jeu ?]

## Decision
[Que faisons-nous et pourquoi ?]

## Consequences
### Positive
[Bénéfices et améliorations]

### Negative
[Compromis et limitations]

### Neutral
[Changements notables qui ne sont ni clairement positifs ni négatifs]
```

---

## Contribuer aux ADRs

1. **Proposer** : Créer un ADR draft avec statut "Proposed"
2. **Discuter** : Partager avec les parties prenantes pour feedback
3. **Décider** : Mettre à jour le statut à "Accepted" quand la décision est prise
4. **Implémenter** : Référencer l'ADR dans le travail d'implémentation
5. **Mettre à jour** : Marquer comme "Deprecated" ou "Superseded" si la décision change

---

## Documentation Connexe

- [Tutoriels](../tutoriel/) — Apprendre en faisant
- [Guides Pratiques](../guide-pratique/) — Accomplir des tâches pratiques
- [Référence](../reference/) — Spécifications techniques

Les ADRs complètent ceux-ci en expliquant la **justification** derrière ce que vous apprenez, faites ou référencez.
