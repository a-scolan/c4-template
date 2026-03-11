## Réponse baseline (old_skill)

## Résumé du Préflight

**Projet actif :** `projects/template/` (projet par défaut, dérivé du template LikeC4)

**Fichiers source of truth :**
- Configuration : [likec4.config.json](projects/template/likec4.config.json)
- Modèle : [system-model.c4](projects/template/system-model.c4)
- Vues : [system-views.c4](projects/template/system-views.c4)
- Specs partagées : [projects/shared/](projects/shared/) (kinds, relations, tags)

**Kinds & Relations disponibles :**
- **Systèmes C1 :** `System_Existing`, `System_New`, `System_External`, `System_Legacy`
- **Containers C2 :** `Container_Api` ✓, `Container_Webapp`, `Container_Database`, `Container_ReverseProxy`, etc.
- **Relations :** `calls`, `reads`, `writes`, `async`, `uses`
- **Tags du container API :** `#Container`, `#Api`

**Plan C1→C2→C3 proposé :**
1. **C1** : Vérifier le système hôte (`mySystem`)
2. **C2** : Ajouter le container API dans `system-model.c4` avec `Container_Api`, relations `calls` (depuis webapp), lien lecture/écriture vers database
3. **C3** : Optionnel — créer composants du nouvel API (contrôleurs, services, etc.)
4. **Views** : Mettre à jour [system-views.c4](projects/template/system-views.c4) pour inclure le nouvel API dans C2

## Auto-évaluation des vérifications effectuées

- ✅ Identification du projet actif (`template`)
- ✅ Localisation des fichiers source of truth (config, model, views, specs partagées)
- ✅ Énumération des kinds C1/C2/C3 et tags applicables
- ✅ Liste des relations de modèle disponibles
- ✅ Structure C1→C2→C3 validée dans le modèle existant
- ✅ Plan séquentiel du système complètement réalisable produit
- ⚠️ *Non effectué : consulter skill `understand-project-structure` (volontairement exclus)*
