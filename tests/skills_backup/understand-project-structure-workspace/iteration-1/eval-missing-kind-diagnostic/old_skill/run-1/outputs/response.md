## Réponse baseline (old_skill)

# Diagnostic structuré pour erreur kind/relationship non reconnu

## 1. **Où vérifier d'abord**
- Le **message d'erreur exact** : identifie le fichier, la ligne, et le symbole problématique
- La **configuration du projet** (`likec4.config.json`) : les includes et spécifications chargées
- Les **fichiers spec** (`spec-*.c4` et `spec-global.c4`) : où les kinds et relationships sont définis

## 2. **Quoi comparer**
- Le kind/relationship utilisé dans le modèle vs. la liste des symboles valides définis dans les specs
- Le chemin FQN (fully qualified name) vs. la hiérarchie d'éléments parent-enfant existants
- Les projets ayant la même configuration pour voir si le symbole s'y trouve

## 3. **Comment confirmer la taxonomie correcte**
- Chercher le symbol dans tous les fichiers spec chargés (grep sur `kind`, `relationship`)
- Vérifier les includes de `likec4.config.json` pour s'assurer que toutes les specs nécessaires sont chargées
- Valider la casse et la syntaxe exacte (LikeC4 est sensible à la casse)
- Consulter les exemples d'utilisation dans d'autres fichiers `.c4` pour le pattern correct

## Checklist d'auto-évaluation
- [ ] Localiser le fichier `.c4` et la ligne du symbole problématique
- [ ] Lister les specs chargées via `likec4.config.json`
- [ ] Chercher la définition du kind/relationship dans `spec-global.c4` et autres specs
- [ ] Comparer la casse et la syntaxe exacte
- [ ] Vérifier que le FQN parent existe si le symbole est un composant/sous-élément
- [ ] Consulter au moins un exemple valide du même type de symbol ailleurs dans le projet
