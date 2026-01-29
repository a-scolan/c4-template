# ADR-0002 : Stratégie de Scalabilité Forgejo Actions

## Statut

Accepté

## Contexte

Le système CI/CD de Dev-Forge (Forgejo Actions) doit scaler pour supporter les équipes de développement sans dégrader les performances ou la fiabilité. Considérations clés :

**Caractéristiques de Charge** :
- Demande variable : Faible la nuit, élevée pendant les heures de bureau
- Pics imprévisibles : Gros merge, nombreux pushes simultanés
- Workflows divers : Linting rapide (< 1 min) à builds lourds (30+ min)
- Variété technologique : Différents langages nécessitent différents environnements

**Contraintes** :
- Infrastructure on-premises (pas d'auto-scaling cloud)
- Limitations budgétaires sur le provisioning de VMs
- Attente des développeurs : Résultats CI/CD dans les 5 minutes pour les workflows typiques
- L'environnement staging doit valider l'architecture production

**Situation Actuelle** :
- Pas d'infrastructure CI/CD déployée
- L'environnement staging est la première cible de déploiement
- Doit démontrer la scalabilité avant le rollout production

### Alternatives Considérées

**Pool de Runners Statique (Pas d'Auto-Scaling)** :
- ✅ Configuration simple
- ✅ Utilisation ressources prévisible
- ❌ Sur-provisioning pour charge pic (gaspillage en période basse)
- ❌ Sous-provisioning risque mise en file et délais
- ❌ Incapable de s'adapter à la croissance organique

**Pool Statique Sur-Provisionné** :
- ✅ Toujours de la capacité disponible
- ❌ Gaspillage ressources significatif (70-80% idle la plupart du temps)
- ❌ Coût d'infrastructure élevé
- ❌ Ne scale pas au-delà du provisioning initial

**Auto-Scaling Basé Kubernetes** :
- ✅ Patterns de scaling cloud-native
- ✅ Allocation ressources fine-grained
- ❌ Nécessite cluster Kubernetes (complexité opérationnelle additionnelle)
- ❌ Surcharge pour petite/moyenne échelle
- ❌ Équipe peu familiarise avec les opérations Kubernetes

**Service CI/CD Externe (GitHub Actions, GitLab SaaS)** :
- ✅ Scaling illimité
- ✅ Pas de gestion d'infrastructure
- ❌ Contredit l'exigence on-premises
- ❌ Préoccupations souveraineté des données
- ❌ Nécessite connectivité Internet sortante
- ❌ Coûts récurrents par minute d'utilisation

## Décision

Nous implémenterons un **pool de runners containerisés avec auto-scaling basé sur la file d'attente** :

### Architecture

**Pool de Base** : 2 runners toujours actifs (environnement staging)
- Fournit disponibilité immédiate pour les tests de validation fonctionnelle
- Baseline minimale assure que le staging reste rentable
- **Le staging valide UNIQUEMENT la fonctionnalité de la plateforme et la correction de la configuration, PAS les exigences de performances ou capacité**

**Contrôleur d'Auto-Scaling** :
- Surveille la profondeur de la file Forgejo Actions toutes les 30 secondes
- Scale up quand profondeur file > 2 (plus de workflows en attente qu'en cours d'exécution)
- Scale down après 5 minutes de temps d'inactivité du runner (gestion efficace des ressources)
- Maximum : 10 runners concurrents (staging), 25 (production)

**Configuration Runners** :
- Exécution basée Docker (workflows containerisés)
- Allocation ressources : 2 vCPU, 4 GB RAM par runner (standard)
- Variante haute-mémoire : 4 vCPU, 8 GB RAM (pour builds lourds)
- Runners éphémères : Détruits après complétion du job (état propre)

### Logique de Scaling

```
if queue_depth > scale_up_threshold:
    active_runners < max_runners:
        provision_new_runner()

if runner_idle_time > scale_down_delay:
    active_runners > base_runner_count:
        decommission_runner()
```

**Paramètres** :
- `base_runner_count` : 2 (staging pour validation fonctionnelle), 8 (production - estimation initiale, à ajuster)
- `max_runner_count` : 10 (staging), 25 (production planifié)
- `scale_up_threshold` : 2 workflows en attente
- `scale_down_delay` : 5 minutes d'inactivité (staging et production)
- `scaling_check_interval` : 30 secondes

### Implémentation

- **Géré par Puppet** : Configuration du pool de runners dans les manifests Puppet
- **Basé VM** : Chaque runner est une VM légère (provisioning rapide ~30-60 secondes)
- **Enregistrement** : Les runners s'auto-enregistrent avec Forgejo au démarrage
- **Monitoring** : Les métriques Prometheus exposent la profondeur de file, l'utilisation des runners

## Conséquences

### Conséquences Positives

- **Rentable** : Payer uniquement pour les VMs exécutant activement des workflows
- **Réactif** : L'auto-scaling réagit en 1-2 minutes après un pic de demande
- **Prévisible** : Le pool de base assure aucun délai de démarrage à froid pour les workflows typiques
- **Dégradation Gracieuse** : Le système de file d'attente fournit une contre-pression naturelle
- **Techno-Agnostique** : L'exécution containerisée supporte tout langage/framework
- **Validé en Staging** : L'environnement staging prouve la scalabilité avant la production
- **Observable** : Les métriques permettent une planification de capacité basée sur les données

### Conséquences Négatives

- **Complexité** : La logique d'auto-scaling ajoute de la complexité opérationnelle vs pool statique
- **Délai de Provisioning** : Lag de 30-60 secondes entre le pic de demande et la disponibilité du runner
- **Surcharge en Ressources** : Surcharge des containers et VMs (vs runners bare-metal)
- **Monitoring Requis** : Doit activement surveiller la file et ajuster les seuils
- **Dépendance Puppet** : Le scaling est fortement couplé à l'automatisation Puppet

### Conséquences Neutres

- **Gestion VM** : Nécessite gestion du cycle de vie des VMs (provisioning, décommissioning)
- **Labels Runners** : Besoin d'une stratégie pour matcher les workflows aux types de runners (standard, haute-mémoire)
- **Gestion de l'État** : Les runners éphémères simplifient le nettoyage mais empêchent la mise en cache (compromis)

## Notes

### Validation Staging

**⚠️ COMPRÉHENSION CRITIQUE : Rôle du Staging**

**Objectif du Staging** : **EXCLUSIVEMENT** validation fonctionnelle du déploiement et de la configuration de la plateforme Dev-Forge. Le staging n'évalue **PAS** les performances, la capacité ou les besoins de scalabilité.

**Ce que le Staging Valide** (correction fonctionnelle uniquement) :
1. ✅ Le provisioning et la logique d'auto-scaling des runners s'exécutent sans erreurs
2. ✅ Les workflows s'exécutent avec succès avec une authentification correcte
3. ✅ Les mécanismes de stockage et récupération des artifacts fonctionnent correctement
4. ✅ L'intégration avec l'interface web Forgejo fonctionne comme prévu
5. ✅ L'automatisation Puppet gère correctement le cycle de vie des runners (provision/décommission)
6. ✅ La connectivité réseau et les règles firewall sont correctement configurées
7. ✅ Les fichiers de configuration et variables d'environnement sont correctement templat és

**Ce que le Staging ne Fait PAS** (cela appartient à la production) :
- ❌ Tests de performance ou benchmarking
- ❌ Validation du dimensionnement ou de la capacité
- ❌ Tests de charge (synthétiques ou réels)
- ❌ Simulation de charge de travail production
- ❌ Évaluation des limites de scalabilité

**Pourquoi c'est Important** : Le staging est délibérément minimal (2 runners de base, max 10) pour minimiser les coûts d'infrastructure tout en prouvant la correction du déploiement. Toute tentative d'utiliser le staging pour évaluer les performances donnerait des résultats sans signification qui ne représentent pas les patterns d'utilisation réels en production.

**Stratégie de Validation des Performances** : La capacité et les caractéristiques de performance en production DOIVENT être mesurées dans l'environnement de production réel avec les charges de travail réelles des projets sur les 30-60 premiers jours. Surveiller la profondeur de la file d'attente, les temps d'attente et l'utilisation des runners, puis ajuster `base_runner_count` et `max_runner_count` en fonction des patterns observés.

### Dimensionnement Production

**Paramètres Production Initiaux** (à ajuster selon utilisation réelle) :
- `base_runner_count` : 8 (estimation initiale conservative, surveiller et ajuster)
- `max_runner_count` : 25 (permet capacité de burst significative)

**Stratégie de Tuning Production** :
- Surveiller la profondeur de file, les temps d'attente et l'utilisation des runners pendant les 30 premiers jours
- Ajuster `base_runner_count` en ciblant 50-70% d'utilisation baseline
- Ajuster `max_runner_count` en assurant que la charge pic ne sature jamais (conserver 20% de marge)
- Revoir les métriques mensuellement et ajuster les paramètres selon les patterns observés

### Déclencheurs de Scaling Alternatifs

Les améliorations futures pourraient scaler selon :
- Heure de la journée (plus de runners pendant les heures de bureau)
- Taille de l'équipe (ajustement automatique quand des développeurs rejoignent)
- Prédiction de durée de workflow (pré-scaling pour les builds lourds connus)

### Décisions connexes

- [ADR-0001 : Plateforme Forgejo](0001-plateforme-forgejo.md) — La plateforme fournit un support Actions natif
- [ADR-0003 : Automatisation Puppet](0003-automatisation-puppet.md) — Puppet orchestre le provisioning des runners
- [ADR-0006 : Neutralité Technologique](0006-neutralite-technologique.md) — L'exécution containerisée permet l'indépendance du langage

### Références

- Patterns de Scaling GitHub Actions : https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/autoscaling-with-self-hosted-runners
- Documentation Forgejo Actions : https://forgejo.org/docs/next/user/actions/
- Feuille de calcul de planification de capacité interne (Confluence : "Capacité Dev-Forge")
