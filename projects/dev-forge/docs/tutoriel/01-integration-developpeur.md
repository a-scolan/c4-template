# Tutoriel : Intégration en tant que Développeur

**Objectif d'Apprentissage** : Créer votre premier dépôt Git sur la plateforme Dev-Forge et effectuer votre commit initial.

**Durée Requise** : 15 minutes  
**Prérequis** : Compte Dev-Forge provisionné par votre administrateur

---

## Ce que Vous Allez Apprendre

À la fin de ce tutoriel, vous aurez :
- Accédé à l'interface web Forgejo
- Créé un nouveau dépôt Git
- Configuré votre client Git local
- Effectué votre premier commit et push vers Dev-Forge

Ce tutoriel vous guide à travers le workflow complet étape par étape. Suivez chaque instruction attentivement—tout ici est conçu pour fonctionner de manière fiable.

---

## Étape 1 : Accéder à Forgejo

Ouvrez votre navigateur web et naviguez vers votre instance Dev-Forge :

```
https://forge.votreentreprise.internal
```

**Vous verrez** la page de connexion Forgejo.

Connectez-vous avec les identifiants fournis par votre administrateur :
- **Nom d'utilisateur** : Votre nom d'utilisateur d'entreprise (généralement le préfixe de votre email)
- **Mot de passe** : Votre mot de passe initial (il vous sera demandé de le changer à la première connexion)

**Remarquez** le tableau de bord qui apparaît après la connexion, montrant l'activité récente et vos dépôts.

---

## Étape 2 : Créer Votre Premier Dépôt

Depuis le tableau de bord, cliquez sur le bouton **"+"** en haut à droite, puis sélectionnez **"New Repository"**.

Remplissez les détails du dépôt :

- **Owner** : Sélectionnez vous-même (votre nom d'utilisateur devrait être pré-sélectionné)
- **Repository Name** : `hello-devforge`
- **Description** : "Mon premier dépôt Dev-Forge"
- **Visibility** : 
  - ✅ **Private** (recommandé pour ce tutoriel)
- **Initialize Repository** :
  - ✅ Cochez "Add a README file"
  - ✅ Cochez "Add .gitignore" et sélectionnez **"None"** dans le menu déroulant
  - ⬜ Laissez "Add a licence" décoché pour l'instant

Cliquez sur **"Create Repository"**.

**Vous verrez** la page de votre nouveau dépôt avec un seul fichier README.md listé.

---

## Étape 3 : Configurer Votre Client Git Local

Ouvrez votre terminal ou invite de commande.

D'abord, dites à Git qui vous êtes (si vous ne l'avez pas encore fait) :

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@entreprise.com"
```

**Vous avez** maintenant configuré votre identité Git. Chaque commit que vous effectuez incluera ces informations.

---

## Étape 4 : Cloner le Dépôt

Sur la page du dépôt Forgejo, trouvez le bouton **"Clone"**. Cliquez dessus et copiez l'URL **HTTPS**. Elle ressemblera à :

```
https://forge.votreentreprise.internal/votrenom/hello-devforge.git
```

Dans votre terminal, naviguez vers l'endroit où vous voulez stocker vos projets :

```bash
cd ~/projects
```

Clonez votre dépôt :

```bash
git clone https://forge.votreentreprise.internal/votrenom/hello-devforge.git
```

Quand demandé pour les identifiants :
- **Username** : Votre nom d'utilisateur Forgejo
- **Password** : Votre mot de passe Forgejo (ou token d'accès personnel si configuré)

Entrez dans le répertoire du dépôt :

```bash
cd hello-devforge
```

**Vous verrez** le contenu du dépôt (juste README.md à ce stade) quand vous exécutez :

```bash
ls
```

---

## Étape 5 : Effectuer Votre Premier Changement

Créez un nouveau fichier pour démontrer un workflow basique :

```bash
echo "Bonjour depuis Dev-Forge!" > hello.txt
```

Vérifiez le statut de votre dépôt :

```bash
git status
```

**Remarquez** que Git montre `hello.txt` comme un fichier non suivi.

Ajoutez le fichier à la zone de staging :

```bash
git add hello.txt
```

Vérifiez le statut à nouveau :

```bash
git status
```

**Vous verrez** que `hello.txt` est maintenant prêt à être commité (affiché en vert).

---

## Étape 6 : Commiter et Pusher

Créez votre premier commit :

```bash
git commit -m "Ajoute hello.txt avec message de salutation"
```

**Vous avez** maintenant enregistré votre changement dans l'historique Git local.

Poussez votre commit vers Dev-Forge :

```bash
git push origin main
```

**Vous verrez** la sortie montrant la progression de l'upload et la confirmation que la branche a été mise à jour.

---

## Étape 7 : Vérifier dans Forgejo

Retournez à votre navigateur web et rafraîchissez la page du dépôt :

```
https://forge.votreentreprise.internal/votrenom/hello-devforge
```

**Remarquez** que :
- Votre fichier `hello.txt` apparaît maintenant dans la liste des fichiers
- Le message de commit "Ajoute hello.txt avec message de salutation" est affiché
- Le nombre de commits a augmenté à 2

Cliquez sur l'onglet **"Commits"** pour voir l'historique complet des commits.

---

## Ce que Vous Avez Accompli

✅ Accédé à Forgejo et créé un dépôt  
✅ Configuré votre environnement Git local  
✅ Cloné un dépôt depuis Dev-Forge  
✅ Effectué un changement local et commité  
✅ Poussé votre travail vers la plateforme  
✅ Vérifié vos changements dans l'interface web

Vous avez maintenant un workflow de développement complet de la machine locale vers Dev-Forge.

---

## Prochaines Étapes

Maintenant que vous maîtrisez les bases, vous êtes prêt à :
- **Continuer l'apprentissage** : Suivez le [tutoriel Premier Pipeline](02-premier-pipeline.md) pour configurer CI/CD
- **Travailler avec du code réel** : Créez un nouveau dépôt pour votre projet actuel
- **Collaborer** : Invitez des membres de l'équipe et apprenez les merge requests (voir les guides pratiques)

---

## Dépannage

**Problème** : Git demande nom d'utilisateur/mot de passe à chaque push  
**Solution** : Configurez le stockage des identifiants Git :
```bash
git config --global credential.helper store
```

**Problème** : Impossible de se connecter à forge.votreentreprise.internal  
**Solution** : Vérifiez que vous êtes sur le réseau d'entreprise ou VPN

**Problème** : "Permission denied" lors du push  
**Solution** : Vérifiez que votre compte a un accès en écriture au dépôt (contactez votre administrateur)

---

## Navigation

⬆️ [Retour aux Tutoriels](../tutoriel/)  
➡️ **Suivant** : [02 - Votre Premier Pipeline CI/CD](02-premier-pipeline.md)
