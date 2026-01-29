# Guide Pratique : Configurer les Runners pour Forgejo Actions

Ce guide vous montre comment configurer et mettre à l'échelle les runners Forgejo Actions pour vos charges de travail CI/CD.

---

## Prérequis

- Accès administrateur à l'infrastructure Dev-Forge
- Compréhension de Forgejo Actions (voir [Tutoriel Premier Pipeline](../tutoriel/02-premier-pipeline.md))
- Accès au dépôt de configuration Puppet

---

## Comprendre l'Architecture des Runners

Dev-Forge utilise des **runners containerisés** qui exécutent les workflows CI/CD dans des environnements isolés. Le pool de runners consiste en :

- **2 runners de base** (configuration staging pour validation fonctionnelle)
- **Auto-scaling** basé sur la profondeur de la file d'attente
- **Exécution basée Docker** pour l'isolation
- **Techno-agnostique** supportant tout langage/framework

---

## Vérifier le Statut Actuel des Runners

### Depuis l'Interface Web Forgejo

1. Naviguez vers **Site Administration** → **Actions** → **Runners**
2. Visualisez les runners actifs avec :
   - Nom et ID du runner
   - Statut (idle, busy, offline)
   - Horodatage dernière activité
   - Nombre de jobs complétés

### Sortie Attendue

Pour un environnement staging sain, vous devriez voir 2 runners avec statut "idle" ou "busy" et horodatages "last seen" récents (dans les 60 secondes).

---

## Configurer le Nombre de Runners

### Ajuster le Pool de Runners de Base

Le nombre de runners de base détermine combien de runners sont toujours disponibles :

**Emplacement de configuration attendu** : Manifest Puppet (`runners.pp`)

**Paramètres attendus** :
```puppet
# Nombre de runners de base (toujours en marche)
$base_runner_count = 2  # Staging : validation fonctionnelle uniquement

# Runners maximum (limite auto-scale)
$max_runner_count = 10  # Staging : suffisant pour validation
```

**Pour modifier** :
1. Mettre à jour le paramètre `$base_runner_count`
2. Appliquer la configuration Puppet (voir [Guide Tâches Puppet](taches-puppet.md))
3. Vérifier que les nouveaux runners apparaissent dans le panneau d'admin Forgejo

**Quand augmenter le nombre de base** :
- Profondeur de file d'attente constamment > 0 pendant les heures normales
- Les workflows attendent fréquemment des runners disponibles
- La taille de l'équipe dépasse 10 développeurs actifs

---

## Configurer l'Auto-Scaling

### Scaling Basé sur la File d'Attente

L'auto-scaling se déclenche quand la file d'attente des workflows dépasse les seuils :

**Configuration attendue** :
```puppet
# Scale up quand la profondeur de file dépasse le seuil
$scale_up_threshold = 2

# Délai de scale down (minutes d'inactivité)
$scale_down_delay = 5  # Staging : gestion efficace des ressources

# Intervalle de vérification (secondes)
$scaling_check_interval = 30
```

**Pour ajuster les seuils** :

**Si les workflows attendent trop longtemps** → Diminuer `$scale_up_threshold` à 1  
**Si les runners se créent/détruisent fréquemment** → Augmenter `$scale_down_delay` à 10  
**Si le scaling réagit lentement** → Diminuer `$scaling_check_interval` à 15

### Vérifier la Scalabilité

Déclencher plusieurs workflows simultanément pour tester l'auto-scaling :

```bash
# Cloner dépôt de test
git clone https://forge.votreentreprise.internal/admin/scaling-test.git
cd scaling-test

# Déclencher 10 workflows concurrents
for i in {1..10}; do
  echo "Exécution test $i" >> test.txt
  git add test.txt
  git commit -m "Déclencher workflow $i"
  git push origin main &
done
wait
```

Surveiller la page **Runners** pour observer :
- Profondeur de file augmentant
- Nouveaux runners apparaissant (dans 1-2 minutes)
- Workflows se distribuant entre les runners
- Runners scalant down après 5 minutes d'inactivité

---

## Configurer les Ressources des Runners

### Allocation CPU et Mémoire

Chaque container runner nécessite des ressources basées sur les workflows typiques :

**Valeurs par défaut attendues** (par runner) :
- **CPU** : 2 vCPU
- **Mémoire** : 4 GB RAM
- **Disque** : 20 GB stockage éphémère

**Pour modifier les limites de ressources** :

Mettre à jour la configuration Puppet :
```puppet
$runner_cpu_limit = '2.0'
$runner_memory_limit = '4G'
$runner_disk_limit = '20G'
```

**Quand augmenter les ressources** :
- Workflows intensifs en build (compilation, packaging)
- Tests gourmands en mémoire (intégration, E2E)
- Checkouts de gros monorepos

**Profils d'exemple** :

| Type de Workflow | CPU | Mémoire | Disque |
|------------------|-----|---------|--------|
| Linting/Tests | 1.0 | 2 GB | 10 GB |
| Build Standard | 2.0 | 4 GB | 20 GB |
| Build Lourd | 4.0 | 8 GB | 50 GB |

---

## Configurer les Labels de Runners

Les labels permettent de cibler des runners spécifiques pour des workflows spécialisés.

**Schéma de labeling attendu** :
- `ubuntu-latest` : Runners Linux par défaut
- `docker` : Runners avec capacité Docker-in-Docker
- `high-memory` : Runners avec 8+ GB RAM
- `gpu` : Runners avec accès GPU (futur)

**Pour ajouter des labels** :

Configurer dans Puppet :
```puppet
forgejo_runner { 'runner-1':
  labels => ['ubuntu-latest', 'docker'],
}

forgejo_runner { 'runner-heavy':
  labels => ['ubuntu-latest', 'docker', 'high-memory'],
  memory => '8G',
  cpu    => '4.0',
}
```

**Utiliser les labels dans les workflows** :
```yaml
jobs:
  build:
    runs-on: high-memory
    steps:
      - name: Tâche de build lourd
        run: make build-large-app
```

---

## Surveiller la Santé des Runners

### Métriques Clés à Suivre

1. **Profondeur de file** : Devrait rester 0-1 pendant les opérations normales
2. **Utilisation des runners** : 40-70% est sain (marge pour les pics)
3. **Taux d'échec des workflows** : < 5% (hors problèmes de code)
4. **Temps d'attente moyen en file** : < 30 secondes

### Vérifier les Métriques

**Depuis le panneau admin Forgejo** :
- Site Administration → Actions → Statistics

**Depuis Prometheus** (si monitoring configuré) :
```
forgejo_actions_queue_depth
forgejo_actions_runner_idle_count
forgejo_actions_runner_busy_count
forgejo_actions_workflow_duration_seconds
```

---

## Dépannage

### Les Runners Montrent Offline

**Vérifier** :
1. Statut du service runner sur la VM : `systemctl status forgejo-runner`
2. Connectivité réseau depuis la VM runner vers le serveur Forgejo
3. Validité du token d'enregistrement du runner

**Résolution** : Voir [Guide Tâches Puppet](taches-puppet.md) pour ré-enregistrer les runners

### Les Workflows Restent en File Indéfiniment

**Vérifier** :
1. Tous les runners sont à capacité (busy)
2. Le workflow spécifie un label indisponible
3. Auto-scaling désactivé ou mal configuré

**Résolution** : Augmenter `$base_runner_count` ou vérifier les paramètres d'auto-scaling

### L'Auto-Scaling Ne Fonctionne Pas

**Vérifier** :
1. Service contrôleur de scaling : `systemctl status forgejo-runner-scaler`
2. Logs du contrôleur : `journalctl -u forgejo-runner-scaler -f`
3. Nombre maximum de runners non atteint

**Résolution** : Vérifier que la configuration Puppet est appliquée et le service redémarré

---

## Prochaines Étapes

- **Optimiser les ressources** : Profiler vos workflows pour dimensionner correctement les ressources des runners
- **Implémenter la surveillance** : Configurer les alertes Prometheus pour la profondeur de file et la santé des runners
- **Planifier la production** : Utiliser les métriques du staging pour dimensionner le pool de runners production (voir ADR-0002)

## Documentation Connexe

- [Référence : Configuration Forgejo](../reference/configuration-forgejo.md)
- [Explication : Stratégie de Scalabilité Actions (ADR-0002)](../../ADR/0002-scalabilite-actions.md)
- [Guide Pratique : Tâches Puppet](taches-puppet.md)

---

## Navigation

🔧 **Autres Guides** : [Configurer Plugins](configurer-plugins.md) | [Tâches Puppet](taches-puppet.md)  
⬆️ [Retour aux Guides Pratiques](../guide-pratique/)  
📖 [Tutoriels](../tutoriel/) | 📋 [Références](../reference/)
