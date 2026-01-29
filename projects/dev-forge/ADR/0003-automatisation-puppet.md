# ADR-0003 : Puppet pour l'Automatisation d'Infrastructure

## Statut

Accepté

## Contexte

Dev-Forge nécessite un provisioning d'infrastructure automatisé et répétable et une gestion de configuration à travers les environnements staging et production. Exigences clés :

**Besoins d'Automatisation** :
- Déployer les serveurs d'application Forgejo
- Provisionner les pools de runners Forgejo Actions
- Configurer les bases de données PostgreSQL
- Gérer les groupes de sécurité réseau et règles firewall
- Maintenir la cohérence de configuration à travers les environnements
- Permettre la réplication rapide d'environnement (staging → production)

**Contexte Organisationnel** :
- **Puppet est déjà utilisé** à travers l'organisation
- Expertise équipe existante dans les manifests et modules Puppet
- Infrastructure Puppet établie (master, agents, r10k)
- Patterns et conventions Puppet organisationnels documentés
- Intégration avec la gestion de secrets existante (Hiera eyaml)

**Contraintes** :
- Doit s'intégrer avec l'automatisation d'infrastructure existante
- Nous ne pouvons pas introduire d'outils nécessitant formation extensive
- Modèle de déploiement on-premises (pas d'APIs de provisioning cloud)
- Doit supporter la parité d'environnement (configs staging/production identiques)

### Alternatives Considérées

**Ansible** :
- ✅ Sans agent (basé SSH)
- ✅ Courbe d'apprentissage plus simple pour débutants
- ✅ Communauté et modules forts
- ❌ **Pas d'expertise organisationnelle existante**
- ❌ Nécessiterait une nouvelle configuration d'infrastructure
- ❌ Paradigme différent des pratiques actuelles

**Terraform** :
- ✅ Infrastructure-as-code déclaratif
- ✅ Excellent pour le provisioning cloud
- ✅ Gestion de l'état pour l'infrastructure
- ❌ **Pas conçu pour la gestion de configuration**
- ❌ Plus faible au déploiement d'application vs provisioning d'infrastructure
- ❌ Pas d'expertise organisationnelle existante

**Configuration Manuelle** :
- ✅ Pas d'apprentissage d'outil requis
- ✅ Contrôle complet
- ❌ Sujet aux erreurs et non répétable
- ❌ Difficile à répliquer staging → production
- ❌ Pas de contrôle de version de configuration
- ❌ Incapable de scaler au-delà du déploiement initial

**SaltStack** :
- ✅ Exécution rapide (transport ZeroMQ)
- ✅ Bonne scalabilité
- ❌ **Pas d'expertise organisationnelle existante**
- ❌ Communauté plus petite que Puppet/Ansible
- ❌ Fragmenterait l'outillage d'automatisation

**Chef** :
- ✅ Gestion de configuration mature
- ✅ DSL Ruby (familier à certains développeurs)
- ❌ **Pas d'expertise organisationnelle existante**
- ❌ Popularité/activité communautaire en déclin
- ❌ Écosystème complexe (Chef Server, workstations)

## Décision

Nous utiliserons **Puppet** pour toute l'automatisation d'infrastructure Dev-Forge et la gestion de configuration.

### Justification

1. **Expertise Existante** : L'équipe est déjà compétente en Puppet—pas de courbe d'apprentissage

2. **Intégration d'Infrastructure** : Exploite le master Puppet existant, les workflows r10k, les secrets Hiera

3. **Patterns Éprouvés** : Peut suivre les conventions organisationnelles établies pour les modules et manifests

4. **Parité d'Environnement** : Hiera permet une configuration identique avec des overrides spécifiques à l'environnement

5. **Contrôle de Version** : Le code Puppet vit naturellement dans Git (s'aligne avec Dev-Forge lui-même étant centré sur Git)

6. **Modèle Déclaratif** : L'abstraction de ressources de Puppet assure la convergence vers l'état désiré

7. **Orchestration** : Puppet orchestrator peut coordonner les déploiements multi-nœuds (database → app → runners)

### Portée

Puppet gérera :
- **Déploiement d'application** : Installation et configuration du service Forgejo
- **Provisioning de base de données** : Installation PostgreSQL, création d'utilisateur, initialisation du schéma
- **Infrastructure des runners** : Provisioning de VM, setup Docker, enregistrement des runners
- **Configuration réseau** : Règles firewall, groupes de sécurité, assignations de zone
- **Agents de monitoring** : Exporters de nœuds Prometheus, shippers de logs
- **Distribution de secrets** : Mots de passe de base de données, tokens API, certificats TLS

Puppet ne gérera **pas** :
- Code/mises à niveau de l'application Forgejo (géré via le mécanisme de mise à jour intégré de Forgejo)
- Stratégies de backup des données (outillage de backup séparé)
- Backend d'agrégation de logs (stack ELK existante)

## Conséquences

### Conséquences Positives

- **Courbe d'Apprentissage Zéro** : L'équipe peut immédiatement écrire des manifests en utilisant les compétences existantes
- **Réutilisation de Modules Existants** : Exploiter la bibliothèque de modules Puppet organisationnelle (PostgreSQL, firewall, etc.)
- **Cohérence d'Infrastructure** : Même outil qui gère le reste de l'infrastructure organisationnelle
- **Gestion de Secrets** : Intégré avec le workflow de chiffrement Hiera eyaml existant
- **Opérations Prévisibles** : Les patterns de déploiement correspondent aux normes organisationnelles
- **Familiarité de Débogage** : L'équipe sait comment troubleshooter les exécutions Puppet
- **Documentation Existe** : Les meilleures pratiques Puppet internes déjà documentées

### Conséquences Négatives

- **Surcharge de l'Agent** : Nécessite un agent Puppet sur chaque nœud géré
- **Dépendance au Master Puppet** : Point de défaillance unique (atténué par le setup HA existant)
- **Dépendance Ruby** : Puppet nécessite un runtime Ruby sur les nœuds
- **Courbe d'Apprentissage pour Nouvelles Recrues** : Puppet moins commun qu'Ansible dans l'industrie
- **Syntaxe Verbeuse** : Les manifests Puppet peuvent être plus verbeux que les playbooks Ansible

### Conséquences Neutres

- **Modèle de Convergence** : Modèle de cohérence éventuelle de Puppet (vs Ansible impératif)
- **Compilation de Catalogue** : Nécessite que le master Puppet compile les catalogues de nœuds
- **Écosystème de Modules** : Puppet Forge a une bonne couverture mais plus petite qu'Ansible Galaxy

## Notes

### Structure de Module Puppet

Le code Puppet Dev-Forge suivra la structure organisationnelle :

```
puppet/modules/devforge/
├── manifests/
│   ├── init.pp              # Classe principale
│   ├── forgejo.pp           # Application Forgejo
│   ├── runners.pp           # Runners Actions
│   ├── database.pp          # PostgreSQL
│   └── networking.pp        # Firewall/sécurité
├── templates/
│   └── app.ini.erb          # Template configuration Forgejo
├── files/
│   └── systemd/             # Fichiers unit systemd
└── hiera/
    ├── staging.yaml         # Paramètres staging
    └── production.yaml      # Paramètres production
```

### Gestion d'Environnement

Hiera hierarchy enables environment differences:

```yaml
# hiera/staging.yaml
devforge::base_runner_count: 3
devforge::database_host: 'db-staging.company.internal'
devforge::domain: 'forge-staging.company.internal'

# hiera/production.yaml
devforge::base_runner_count: 8
devforge::database_host: 'db-prod.company.internal'
devforge::domain: 'forge.company.internal'
```

### Points d'Intégration

- **r10k** : Code Puppet Dev-Forge déployé via le workflow r10k existant
- **PuppetDB** : Interroger l'état de l'infrastructure pour monitoring/reporting
- **Foreman** : (si utilisé) Le provisioning VM déclenche la classification Puppet
- **Hiera** : Secrets gérés via l'infrastructure eyaml existante

### Alternatives pour Tâches Spécifiques

Bien que Puppet soit l'outil principal, certaines tâches peuvent utiliser des outils spécialisés :
- **Renouvellement de certificat TLS** : Cert-manager existant ou client ACME
- **Orchestration de backup** : Solution de backup existante (Bacula, Bareos, etc.)
- **Monitoring** : Infrastructure Prometheus/Grafana existante

### Décisions connexes

- [ADR-0002 : Scalabilité Actions](0002-scalabilite-actions.md) — Puppet orchestre l'auto-scaling des runners
- [ADR-0005 : Zones Réseau](0005-zones-reseau.md) — Puppet applique la segmentation réseau

### Références

- Guide de Style Puppet Organisationnel (Confluence : "Infrastructure/Puppet")
- Meilleures Pratiques Puppet : https://puppet.com/docs/puppet/latest/style_guide.html
- Modules Puppet Existants : Dépôt GitLab/Forgejo interne
