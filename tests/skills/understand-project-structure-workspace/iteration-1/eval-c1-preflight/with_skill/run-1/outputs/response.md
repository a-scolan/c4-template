## Réponse with_skill

## ✅ Preflight Complet - Analyse du Workspace

### **Projet Actif: `template`**
Codebase à 2 projets LikeC4:
- **`template`** (principal) - Modèle de base avec C1/C2/C3
- **`spec-showcase`** - Référence d'implémentation

### **Kinds Disponibles pour Containers**
| Kind | Notation | Usage |
|------|----------|-------|
| `Container_Api` | API / Service | ✅ Pour votre nouveau container |
| `Container_Spa` | Single Page App | Interface frontend |
| `Container_Webapp` | Web App | Webapp classique |
| `Container_Queue` | Message Queue | Async processing |
| `Container_Database` | Database | Persistence |
| `Container_ReverseProxy` | Reverse proxy | Ingress tier |

**Source:** [projects/shared/spec-containers.c4](projects/shared/spec-containers.c4)

### **Relationship Types Disponibles**
- `calls` (HTTP/sync) - bleu/solid
- `async` (message queue) - bleu/dashed  
- `reads` (query) - vert
- `writes` (update) - ambre
- `uses` (generic) - gris

### **Tags Recommandés**
- **Purpose:** `#Internal`, `#External`, `#Legacy`
- **Platform:** `#Cloud`, `#Saas`
- **Tech:** `#Queue`, `#Security`

**Source:** [projects/shared/spec-global.c4](projects/shared/spec-global.c4)

### **C1→C2→C3 Plan d'Ajout d'API Container**

**ÉTAT ACTUEL (template):**
```
C1: Actor_Person 'User' → System_Existing 'mySystem' ← System_External 'emailService'
C2: webapp (Container_Webapp) → api (Container_Api) → database (Container_Database)
              ↓ (calls HTTPS)       ↓ (reads/writes)
```

**PLAN D'AJOUT NOUVEAU API CONTAINER:**

| Étape | Niveau | Action | Fichier |
|-------|--------|--------|---------|
| 1 | C1 | S'il y a nouvel **acteur externe**, l'ajouter dans `system-model.c4` | system-model.c4 |
| 2 | C2 | Créer `Container_Api 'New API'` dans bloc `mySystem { }` | system-model.c4 |
| 3 | C2 | Connecter avec `webapp -[calls]-> newApi` ou `api -[async]-> newApi` | system-model.c4 |
| 4 | C2 | Créer view dans `views 'C2'` montrant tous containers + relationships | system-views.c4 |
| 5 | C3 | *(Optionnel)* Détailler internes si complexe = `Component_Service` | system-model.c4 |

**Fichiers source of truth:**
- [projects/template/system-model.c4](projects/template/system-model.c4) - Modèle logique
- [projects/template/system-views.c4](projects/template/system-views.c4) - Visualisations
- [projects/template/likec4.config.json](projects/template/likec4.config.json) - Config includes

## ✅ Checklist Vérifications Effectuées

- ✅ Projet actif identifié (`template`)
- ✅ Structure multi-projet validée  
- ✅ Spec-*.c4 partagées lues (global, context, containers)
- ✅ Element kinds C2 énumérés (Container_Api disponible)
- ✅ Relationship types disponibles (calls, async, reads, writes)
- ✅ Tags spécification (purpose, platform, tech)
- ✅ C1/C2/C3 actuel du template catalogué
- ✅ Fichiers source of truth localisés
- ✅ Plan C1→C2→C3 défini (5 étapes)
