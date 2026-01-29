# Tutoriel : Votre Premier Pipeline CI/CD

**Objectif d'Apprentissage** : Créer et exécuter votre premier pipeline automatisé en utilisant Forgejo Actions.

**Durée Requise** : 20 minutes  
**Prérequis** : 
- Tutoriel 01 terminé : [Intégration en tant que Développeur](01-integration-developpeur.md)
- Avoir un dépôt sur Dev-Forge (nous utiliserons `hello-devforge` du Tutoriel 01)

---

## Ce que Vous Allez Apprendre

À la fin de ce tutoriel, vous aurez :
- Créé un fichier de workflow Forgejo Actions
- Déclenché un pipeline automatisé
- Visualisé les logs d'exécution du pipeline
- Compris la structure de base d'un workflow CI/CD

Ce tutoriel introduit les concepts CI/CD à travers la pratique. Chaque étape produira des résultats visibles que vous pouvez vérifier.

---

## Étape 1 : Comprendre Forgejo Actions

Forgejo Actions est le système CI/CD intégré de Dev-Forge. Il exécute automatiquement des tâches quand vous poussez du code, comme :
- Exécuter des tests
- Builder des applications
- Déployer vers des environnements
- Vérifier la qualité du code

Les workflows sont définis dans des fichiers YAML stockés dans votre dépôt sous `.forgejo/workflows/`.

**Vous êtes** sur le point de créer votre premier fichier de workflow.

---

## Étape 2 : Créer le Répertoire de Workflow

Dans votre terminal, naviguez vers votre dépôt `hello-devforge` :

```bash
cd ~/projects/hello-devforge
```

Créez la structure de répertoire pour les workflows :

```bash
mkdir -p .forgejo/workflows
```

**Vous avez** créé l'emplacement standard où Forgejo cherche les définitions d'automatisation.

---

## Étape 3 : Créer Votre Premier Workflow

Créez un nouveau fichier de workflow :

```bash
nano .forgejo/workflows/hello.yml
```

Copiez et collez cette définition de workflow :

```yaml
name: Hello Workflow

on:
  push:
    branches:
      - main

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Say hello
        run: echo "Bonjour depuis Forgejo Actions!"
      
      - name: Show files
        run: ls -la
      
      - name: Display hello.txt
        run: cat hello.txt
```

Sauvegardez et quittez (dans nano : `Ctrl+X`, puis `Y`, puis `Entrée`).

**Remarquez** la structure :
- **name** : Nom lisible du workflow
- **on** : Condition de déclenchement (s'exécute sur les pushes vers la branche `main`)
- **jobs** : Un ou plusieurs jobs à exécuter
- **steps** : Commandes individuelles dans un job

---

## Étape 4 : Commiter et Pusher le Workflow

Ajoutez le nouveau fichier de workflow à Git :

```bash
git add .forgejo/workflows/hello.yml
```

Commitez le workflow :

```bash
git commit -m "Ajoute premier workflow CI/CD"
```

Poussez vers Dev-Forge :

```bash
git push origin main
```

**Vous avez** juste déclenché votre premier pipeline automatisé ! Le push vers la branche `main` active le workflow.

---

## Étape 5 : Visualiser l'Exécution du Pipeline

Ouvrez votre dépôt dans Forgejo :

```
https://forge.votreentreprise.internal/votrenom/hello-devforge
```

Cliquez sur l'onglet **"Actions"** dans la navigation du dépôt.

**Vous verrez** votre exécution de workflow listée avec :
- Nom du workflow : "Hello Workflow"
- Message de commit : "Ajoute premier workflow CI/CD"
- Indicateur de statut (⏳ en cours, ✅ succès, ou ❌ échec)

Cliquez sur l'exécution du workflow pour voir les détails.

---

## Étape 6 : Explorer les Logs

Dans la page de détails de l'exécution du workflow :

1. **Vous verrez** le job `greet` listé
2. Cliquez sur le job `greet` pour l'étendre
3. **Remarquez** chaque étape de votre fichier de workflow :
   - "Checkout code"
   - "Say hello"
   - "Show files"
   - "Display hello.txt"

Cliquez sur l'étape **"Say hello"**.

**Vous verrez** la sortie :
```
Bonjour depuis Forgejo Actions!
```

Cliquez sur l'étape **"Display hello.txt"**.

**Vous verrez** le contenu :
```
Bonjour depuis Dev-Forge!
```

**Vous avez** exécuté et surveillé avec succès un workflow automatisé.

---

## Étape 7 : Déclencher le Workflow à Nouveau

Effectuez un autre petit changement pour voir le pipeline s'exécuter à nouveau :

```bash
echo "Test du pipeline" >> hello.txt
```

Commitez et poussez :

```bash
git add hello.txt
git commit -m "Test du déclenchement du pipeline"
git push origin main
```

Retournez à l'onglet **Actions** dans Forgejo.

**Remarquez** qu'une deuxième exécution de workflow a démarré automatiquement. Cela démontre que les workflows se déclenchent à chaque push vers `main`.

---

## Étape 8 : Comprendre Ce Qui S'est Passé

Revoyons ce que fait le workflow :

1. **Forgejo a détecté** votre push vers la branche `main`
2. **Un runner** (environnement d'exécution containerisé) a été assigné
3. **L'étape Checkout** a cloné votre dépôt dans le runner
4. **Les étapes personnalisées** ont exécuté vos commandes séquentiellement
5. **Les logs** ont capturé toute la sortie pour le débogage
6. **Le statut** a rapporté le succès ou l'échec à Forgejo

Le processus entier s'est déroulé automatiquement sans intervention manuelle.

---

## Ce que Vous Avez Accompli

✅ Créé un fichier de workflow Forgejo Actions  
✅ Déclenché CI/CD automatiquement lors du push de code  
✅ Visualisé les logs d'exécution en temps réel  
✅ Compris le modèle workflow → runner → exécution  
✅ Vérifié la répétition automatisée sur les pushes suivants

Vous comprenez maintenant les fondations de l'automatisation CI/CD sur Dev-Forge.

---

## Prochaines Étapes

Maintenant que vous comprenez les pipelines de base, vous pouvez :
- **Étendre votre workflow** : Ajouter des étapes de tests, linting ou build spécifiques à votre technologie
- **Apprendre les fonctionnalités avancées** : Voir le [Guide Pratique de Configuration des Runners](../guide-pratique/configurer-runners.md) pour les stratégies de scaling
- **Implémenter du vrai CI/CD** : Consultez la [Référence de Configuration Forgejo](../reference/configuration-forgejo.md) pour les options de runners disponibles

---

## Patterns Courants à Explorer

Une fois à l'aise, vous pouvez étendre votre workflow pour inclure :

**Tests** (exemple pour Python) :
```yaml
- name: Run tests
  run: |
    pip install pytest
    pytest tests/
```

**Build** (exemple pour Node.js) :
```yaml
- name: Build application
  run: |
    npm install
    npm run build
```

**Déploiement** (exemple utilisant SSH) :
```yaml
- name: Deploy to staging
  run: |
    scp -r ./build user@staging:/var/www/app
```

Ces exemples démontrent la nature techno-agnostique de Dev-Forge—utilisez n'importe quel langage ou framework.

---

## Dépannage

**Problème** : Le workflow n'apparaît pas dans l'onglet Actions  
**Solution** : Vérifiez que le fichier est dans `.forgejo/workflows/` (notez le préfixe point) et a l'extension `.yml` ou `.yaml`

**Problème** : Le pipeline échoue immédiatement  
**Solution** : Vérifiez les logs pour des erreurs de syntaxe YAML. Utilisez un validateur YAML en ligne pour vérifier votre fichier de workflow

**Problème** : "No runners available"  
**Solution** : Contactez votre administrateur—le pool de runners peut nécessiter un scaling (voir ADR-0002 pour les détails d'architecture)

**Problème** : Les étapes s'exécutent mais ne produisent pas la sortie attendue  
**Solution** : Vérifiez que les commandes fonctionnent dans votre terminal local d'abord, puis répliquez exactement dans les étapes du workflow

---

## Navigation

⬅️ **Précédent** : [01 - Intégration en tant que Développeur](01-integration-developpeur.md)  
⬆️ [Retour aux Tutoriels](../tutoriel/)  
🔧 **Poursuivre** : [Guides Pratiques](../guide-pratique/) pour des tâches avancées
