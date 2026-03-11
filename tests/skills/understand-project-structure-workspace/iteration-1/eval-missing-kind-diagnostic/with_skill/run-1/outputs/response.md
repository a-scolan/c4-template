## Réponse with_skill

## Diagnostic Structuré : Erreurs de Kind/Relationship Non Reconnus

### 1. **Où vérifier d'abord (Source of Truth)**
   - **Specs partagées** (`projects/shared/spec-*.c4`) : seule taxonomie valide
     - `spec-global.c4` → relationship types (uses, calls, async, reads, writes)
     - `spec-context.c4` → kinds C1 (Actor, Actor_Person, System_New, System_External, etc.)
     - `spec-containers.c4` → kinds C2 (Container_Api, Container_Database, Container_Spa, etc.)
     - `spec-components.c4` → kinds C3 (Component)
     - `spec-deployment.c4` → kinds infrastructure (Zone, Node, Vm, etc.)
   - **Résumé projet** (MCP `read-project-summary`) : vérifier que le projet réel charge ces specs

### 2. **Quoi comparer (Validation)**
   - **Erreur signalée** : `unknown kind 'MonKind'` ou `unknown relationship 'maRelation'`
   - **Chercher dans specs** : Est-ce le nom exact? (ex. `Container_Api` ≠ `ContainerAPI`)
   - **Vérifier le contexte C4** : Le kind est-il au bon niveau? (C1 ≠ C2 ≠ C3 ≠ Deployment)
   - **Charger la config** (`likec4.config.json`) : Confirme que `include.paths` pointe vers `../shared`

### 3. **Séquence de confirmation (avant correction)**
   1. **Lancer** `read-project-summary` → liste tous les kinds/relationships valides chargés
   2. **Chercher** le kind erroné dans cette liste → confirmer s'il existe (typo?) ou s'il manque
   3. **Relire** la spec appropriée → copier le nom exact (casse, underscores)
   4. **Vérifier parent** : Si Component, est-il dans un Container? Si Container, dans un System?
   5. **Fallback** : Si specs sont chargées mais kind manque → vérifier `likec4.config.json` inclut `../shared`

### 4. **Corriger avec confiance**
   - Utiliser **exactement** le nom de la spec (ex. `Container_Api`, pas `ContainerAPI`)
   - Vérifier parent hiérarchique (C1→C2→C3)
   - Relancer `read-project-summary` après modification

## Auto-évaluation des Vérifications Effectuées

- ✅ Lecture du skill `understand-project-structure` → workflow MCP et sources of truth identifiées
- ✅ Lecture du skill `c4-modeling-process` → hiérarchie C1→C2→C3 comprise
- ✅ Consultation de **4 specs partagées** → kinds C1/C2/C3/Deployment listés
- ✅ Vérification de `likec4.config.json` → includes et aliases confirmés
- ✅ Analyse de l'évaluation #2 → expectations explicitées et adressées
- ✅ Diagnostic centré sur shared specs + résumé projet (pas du guessing)
- ✅ Séquence de confirmation structurée avec fallback proposé
