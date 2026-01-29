# Guide Pratique : Tâches Puppet pour Dev-Forge

Ce guide fournit les résultats attendus pour les tâches de déploiement courantes pilotées par Puppet sans détailler l'implémentation (les pratiques Puppet organisationnelles existantes s'appliquent).

---

## Prérequis

- Accès au dépôt de contrôle Puppet
- Compréhension des conventions Puppet organisationnelles
- Permissions pour déclencher les exécutions Puppet

---

## Déployer l'Instance Forgejo

### Résultat Attendu

Une instance Forgejo entièrement configurée :
- Service s'exécutant sur la VM désignée
- Base de données PostgreSQL initialisée
- Fichier de configuration (`app.ini`) déployé avec les valeurs par défaut organisationnelles
- Certificat HTTPS configuré
- Intégration reverse proxy/load balancer complète

### Déclencher le Déploiement

```bash
# Appliquer le manifest Puppet pour Forgejo
puppet agent -t --tags forgejo
```

### Vérification

Après la fin de l'exécution Puppet :
- Service accessible à `https://forge.entreprise.internal`
- Endpoint health check retourne 200 : `curl -I https://forge.entreprise.internal/api/healthz`
- Compte admin créé (identifiants dans le système de gestion des secrets)

---

## Déployer les Runners Forgejo Actions

### Résultat Attendu

Pool de runners déployé selon la configuration :
- Nombre spécifié de VMs runner provisionnées (2 pour staging)
- Runtime Docker installé et configuré
- Runners enregistrés avec l'instance Forgejo
- Service contrôleur d'auto-scaling actif
- Connectivité réseau vers le serveur Forgejo vérifiée

### Déclencher le Déploiement

```bash
# Déployer l'infrastructure des runners
puppet agent -t --tags forgejo-runners
```

### Vérification

- Les runners apparaissent dans le panneau d'admin Forgejo : **Site Administration** → **Actions** → **Runners**
- Le statut des runners montre "idle"
- Un workflow de test s'exécute avec succès (voir [Tutoriel Premier Pipeline](../tutoriel/02-premier-pipeline.md))

---

## Mettre à l'Échelle le Pool de Runners

### Résultat Attendu

Nombre de runners ajusté pour répondre aux demandes de charge de travail :
- VMs runner additionnelles provisionnées (ou décommissionnées)
- Chaque runner enregistré avec un identifiant unique
- Configuration du load balancer mise à jour (si applicable)
- Alertes de monitoring ajustées pour la nouvelle capacité

### Déclencher le Scaling

```bash
# Mettre à l'échelle le pool de runners (nombre défini dans les paramètres Puppet)
puppet agent -t --tags forgejo-runners-scale
```

### Vérification

- Le nouveau nombre de runners correspond à la configuration des paramètres
- Tous les runners montrent le statut "idle" ou "busy" (pas de runners offline)
- La profondeur de file diminue sous charge (voir [Configurer les Runners](configurer-runners.md))

---

## Mettre à Jour la Configuration Forgejo

### Résultat Attendu

Changements de configuration appliqués sans interruption de service :
- `app.ini` mis à jour déployé sur le serveur Forgejo
- Service rechargé gracieusement (ou redémarré si requis)
- Sessions actives préservées (quand possible)
- Entrée de log d'audit créée

### Déclencher la Mise à Jour

```bash
# Appliquer les changements de configuration
puppet agent -t --tags forgejo-config
```

### Vérification

- Changements de configuration visibles : `sudo grep "<paramètre_changé>" /etc/forgejo/app.ini`
- Service reste sain : `systemctl status forgejo`
- Interface web accessible et fonctionne normalement

---

## Déployer la Base de Données PostgreSQL

### Résultat Attendu

Instance PostgreSQL dédiée pour Forgejo :
- Service PostgreSQL s'exécutant sur la VM désignée
- Base de données et utilisateur créés avec les permissions appropriées
- Pooling de connexions configuré (si utilisation de PgBouncer)
- Sauvegardes programmées et vérifiées
- Règles de firewall réseau n'autorisent que les connexions du serveur Forgejo

### Déclencher le Déploiement

```bash
# Déployer PostgreSQL pour Forgejo
puppet agent -t --tags forgejo-database
```

### Vérification

- Base de données accessible depuis le serveur Forgejo : `psql -h db.entreprise.internal -U forgejo -d forgejo -c "SELECT 1;"`
- Forgejo se connecte avec succès (vérifier les logs) : `sudo journalctl -u forgejo -n 50`
- Schéma initial créé (les tables existent)

---

## Configurer la Sécurité Réseau

### Résultat Attendu

Zones réseau et règles de firewall établies :
- **Zone DMZ** : Reverse proxy/load balancer accessible depuis Internet
- **Zone AppTier** : Serveur Forgejo isolé, accepte uniquement depuis DMZ
- **Zone DataTier** : PostgreSQL isolé, accepte uniquement depuis AppTier
- Règles de firewall appliquées aux frontières de zones
- Assignations de groupes de sécurité vérifiées

### Déclencher la Configuration

```bash
# Appliquer la politique de sécurité réseau
puppet agent -t --tags network-security
```

### Vérification

- Tester l'accès externe : `curl https://forge.entreprise.internal` (succède)
- Tester l'accès direct à la base de données depuis l'extérieur : `psql -h db.entreprise.internal` (échoue/timeout)
- Examiner les logs de firewall pour les tentatives refusées
- Vérifier l'appartenance aux groupes de sécurité dans le tableau de bord infrastructure

---

## Provisionner l'Environnement Staging

### Résultat Attendu

Environnement staging complet déployé :
- Toutes les VMs provisionnées dans la zone réseau staging
- Services Forgejo, runners et base de données déployés
- La configuration utilise des paramètres spécifiques au staging
- Agents de monitoring installés et rapportant
- Environnement tagué pour identification (`environment=staging`)

### Déclencher le Provisioning

```bash
# Déployer l'environnement staging complet
puppet agent -t --environment staging --tags devforge-full
```

### Vérification

- Tous les services sains dans le tableau de bord monitoring
- Peut compléter un workflow end-to-end :
  1. Créer un dépôt
  2. Pusher du code avec workflow CI/CD
  3. Vérifier que le pipeline s'exécute
  4. Merger une pull request
- Environnement isolé de la production (VLANs/subnets séparés)

---

## Sauvegarde et Restauration

### Résultat Attendu (Sauvegarde)

Sauvegarde automatisée des données critiques :
- Base de données PostgreSQL sauvegardée quotidiennement
- Dépôts Forgejo sauvegardés vers object storage
- Fichiers de configuration versionnés dans dépôt de sauvegarde
- Tests de vérification de sauvegarde réussis
- Politique de rétention appliquée (staging : 7 jours)

### Résultat Attendu (Restauration)

Système restauré depuis sauvegarde :
- Base de données restaurée à un point dans le temps spécifié
- Dépôts restaurés depuis sauvegarde
- Configuration réappliquée
- Validation du service confirme l'intégrité

### Déclencher la Sauvegarde

```bash
# La sauvegarde est automatisée, mais peut être déclenchée manuellement
puppet agent -t --tags forgejo-backup
```

### Déclencher la Restauration

```bash
# Restaurer depuis la dernière sauvegarde
puppet agent -t --tags forgejo-restore
```

### Vérification (Restauration)

- Les données restaurées correspondent au timestamp attendu
- Vérification aléatoire d'un dépôt montre l'historique complet
- Comptes utilisateurs et permissions intacts
- Tous les services reviennent à l'état opérationnel

---

## Dépannage

### L'Exécution Puppet Échoue

**Vérifier** :
- Statut du service agent Puppet : `systemctl status puppet`
- Connectivité au serveur Puppet : `puppet agent -t --noop`
- Rapport de dernière exécution : `puppet agent --last-run-report`

**Résolution** : Examiner les logs Puppet pour l'erreur spécifique, vérifier la connectivité réseau vers le serveur Puppet

### Le Service Ne Démarre Pas Après Déploiement

**Vérifier** :
- Statut du service : `systemctl status <service>`
- Logs du service : `journalctl -u <service> -n 100`
- Syntaxe de configuration : Pour Forgejo, `forgejo --check`

**Résolution** : Vérifier la syntaxe de configuration, vérifier les permissions de fichiers, examiner le fichier unit systemd

### La Configuration N'Est Pas Appliquée

**Vérifier** :
- L'exécution Puppet s'est terminée avec succès (exit code 0)
- Fichier cible modifié : `ls -l /etc/forgejo/app.ini`
- Contenu du fichier : `grep "<paramètre>" /etc/forgejo/app.ini`

**Résolution** : Vérifier que les facts Puppet sont corrects (`facter`), vérifier que la version du module correspond à l'attente

---

## Structure Attendue du Module Puppet

*Pour référence* — l'implémentation réelle suit les conventions organisationnelles :

```
puppet/modules/devforge/
├── manifests/
│   ├── forgejo.pp          # Déploiement application Forgejo
│   ├── runners.pp          # Déploiement runners Actions
│   ├── database.pp         # Configuration PostgreSQL
│   └── networking.pp       # Groupes de sécurité et firewall
├── templates/
│   └── app.ini.erb         # Template configuration Forgejo
├── files/
│   └── systemd/            # Fichiers unit systemd
└── hiera/
    ├── staging.yaml        # Paramètres environnement staging
    └── production.yaml     # Paramètres environnement production
```

---

## Prochaines Étapes

- **Valider les déploiements** : Utiliser le monitoring pour vérifier la santé des services
- **Automatiser davantage** : Intégrer les exécutions Puppet dans les pipelines CI/CD
- **Documenter les personnalisations** : Maintenir la documentation des conventions Puppet organisationnelles

## Documentation Connexe

- [Guide Pratique : Configurer les Runners](configurer-runners.md) — Configuration spécifique aux runners
- [Guide Pratique : Configurer les Plugins](configurer-plugins.md) — Activation des plugins post-déploiement
- [Explication : Automatisation Puppet (ADR-0003)](../../ADR/0003-automatisation-puppet.md) — Justification de la stratégie d'automatisation

---

## Navigation

🔧 **Autres Guides** : [Configurer Runners](configurer-runners.md) | [Configurer Plugins](configurer-plugins.md)  
⬆️ [Retour aux Guides Pratiques](../guide-pratique/)  
📖 [Tutoriels](../tutoriel/) | 📋 [Références](../reference/)
