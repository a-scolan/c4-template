# ADR-0006 : Principe de Neutralité Technologique

## Statut

Accepté

## Contexte

Dev-Forge sert des équipes de développement travaillant avec des langages de programmation, frameworks et toolchains divers. La plateforme ne doit pas imposer de contraintes techniques ou favoriser des écosystèmes spécifiques.

**Diversité des Équipes** :
- Backend : Java (Spring Boot), Python (Django, Flask), Go, Node.js
- Frontend : React, Vue.js, Angular, JavaScript vanilla
- Mobile : Swift, Kotlin, React Native
- Infrastructure : Terraform, Ansible, scripts shell
- Data : Python (pandas, scikit-learn), R, SQL

**Défis Historiques** :
- Les outils internes précédents favorisaient des langages spécifiques (CI/CD centré Java)
- Les développeurs évitaient la plateforme en raison du mauvais support de leur stack
- Les contournements personnalisés créaient une charge de maintenance
- Les équipes construisaient des solutions shadow IT en dehors de la plateforme officielle

**Exigences** :
- Supporter tout langage/framework sans configuration spéciale
- Pas de suppositions intégrées sur les outils de build ou gestionnaires de packages
- Permettre les projets polyglot (plusieurs langages dans un dépôt)
- Permettre aux équipes d'adopter de nouvelles technologies sans changements de plateforme

### Alternatives Considérées

**Optimisations Spécifiques au Langage** :
- ✅ Expérience de classe mondiale pour les langages supportés
- ✅ Templates et patterns intégrés
- ❌ **Exclut les équipes utilisant d'autres stacks**
- ❌ Nécessite des mises à jour de plateforme pour l'adoption de nouveaux langages
- ❌ Crée un stigmate de citoyen de seconde classe pour les langages non supportés

**Liste de Technologies Restreinte** :
- ✅ Simplifie le support et le troubleshooting
- ✅ La standardisation réduit la complexité
- ❌ **Étouffe l'innovation et l'expérimentation**
- ❌ Force les choix technologiques sur les équipes
- ❌ La plateforme devient un goulot d'étranglement pour les nouveaux outils

**Services Par-Langage** :
- ✅ Services spécialisés pour chaque écosystème
- ✅ Intégration profonde (dépôt Maven, registry npm séparés)
- ❌ Complexité opérationnelle élevée (nombreux services à maintenir)
- ❌ Expérience utilisateur inconsistante entre langages
- ❌ Scale mal alors que le paysage technologique évolue

**Containerisation Uniquement** :
- ✅ Flexibilité maximale (apportez votre propre container)
- ✅ Language-agnostique par design
- ❌ Courbe d'apprentissage raide (nécessite expertise Docker)
- ❌ Surcharge pour projets simples
- ❌ Ne résout pas l'intégration du package registry

## Décision

Dev-Forge adhérera à un **principe de neutralité technologique strict** :

### Principes Fondamentaux

**1. Pas de Suppositions sur le Langage**
- La plateforme ne fait aucune supposition sur le langage ou framework du projet
- Aucune configuration spéciale requise pour tout langage
- Aucune technologie "bénie" ou "préférée" promue

**2. Infrastructure Générique**
- Les runners CI/CD fournissent des environnements Linux génériques (Ubuntu LTS)
- Les workflows spécifient leurs dépendances explicitement (non pré-installées)
- Les registries de packages supportent tous les écosystèmes majeurs également

**3. Apportez Votre Propre Toolchain**
- Les projets définissent leurs outils de build/test/deploy dans les fichiers workflow
- Pas de systèmes de build ou conventions imposés par la plateforme
- Les équipes choisissent les outils basés sur les exigences, pas les limitations de plateforme

**4. Support Polyglot**
- Un seul dépôt peut contenir plusieurs langages
- Les workflows CI/CD gèrent les stacks technologiques mixtes
- Pas de frontières artificielles entre écosystèmes

### Implémentation

#### CI/CD (Forgejo Actions)

**Image Runner Générique** : `ubuntu-latest`
```yaml
# Exemple : projet Node.js
- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '18'

# Exemple : projet Python  
- name: Setup Python
  uses: actions/setup-python@v3
  with:
    python-version: '3.11'

# Exemple : projet Java
- name: Setup Java
  uses: actions/setup-java@v3
  with:
    java-version: '17'
    distribution: 'temurin'
```

**Pattern Clé** : Les workflows déclarent explicitement les dépendances—la plateforme fournit le primitif, les projets fournissent la spécificité.

#### Package Registry (Intégration Nexus)

**Support Écosystème** :
- npm (JavaScript/TypeScript)
- Maven (Java)
- PyPI (Python)
- NuGet (.NET)
- Docker (containers)
- (Futur : RubyGems, Cargo, modules Go)

**Accès Uniforme** : `https://forge.company.internal/api/packages/{ecosystem}/`

**Authentification** : Mêmes credentials quel que soit l'écosystème

**Pas de Préférence** : Tous les écosystèmes également supportés, pas de langage "primaire"

#### Gestion de Dépôt

**Pas de Détection de Langage** :
- La plateforme n'analyse pas le code pour déterminer le langage
- Pas de génération automatique de badge basée sur le type de projet
- Pas de fonctionnalités spécifiques au langage dans le navigateur de dépôt

**Format de Fichier Agnostique** :
- Coloration syntaxique pour tous les langages (via bibliothèque universelle)
- Pas de suppositions sur les fichiers de build (package.json, pom.xml, etc.)

#### Documentation & Exemples

**Docs Neutres au Langage** :
- Les tutoriels montrent des workflows pour plusieurs langages (exemples Node.js, Python, Go)
- Les guides how-to évitent les conseils spécifiques au langage
- La documentation de référence couvre la configurabilité, pas les conventions

**Contributions Communautaires** :
- Dépôts template pour stacks communes (pilotés par la communauté)
- Pas de recommandations officielles de plateforme—juste des exemples

## Conséquences

### Conséquences Positives

- **Adoption Universelle** : Toute équipe peut utiliser la plateforme quel que soit son stack tech
- **À l'Épreuve du Futur** : Nouveaux langages/frameworks supportés sans changements de plateforme
- **Favorable à l'Innovation** : Les équipes peuvent expérimenter avec des technologies émergentes
- **Pas de Vendor Lock-In** : La plateforme ne dicte pas les choix technologiques
- **Expérience Cohérente** : Mêmes workflows/patterns s'appliquent à tous les langages
- **Biais Réduit** : Élimine la perception de favoritisme envers des écosystèmes spécifiques
- **Opérations Simplifiées** : Un environnement d'exécution (Linux) supporte tout

### Conséquences Négatives

- **Pas d'Optimisation** : Ne permet pas d'optimiser profondément pour les spécificités de langages spécifiques
- **Courbe d'Apprentissage** : Les équipes doivent configurer leur propre toolchain (pas pré-configuré)
- **Prolifération de Templates** : Besoin de nombreux exemples pour couvrir tous les langages
- **Complexité du Support** : L'équipe de support doit comprendre des écosystèmes divers
- **Troubleshooting** : Plus difficile de diagnostiquer les problèmes spécifiques au langage
- **Utilisation Ressources** : Certains workflows inefficaces en raison de la surcharge d'installation du runtime

### Conséquences Neutres

- **Responsabilité Communautaire** : Les équipes contribuent des exemples pour leurs stacks
- **Charge de Documentation** : Plus d'exemples nécessaires pour couvrir les cas communs
- **Variabilité de Performance** : La vitesse du workflow dépend du temps de téléchargement du toolchain

## Notes

### Acceptable Exceptions

Neutrality is not absolutism. Acceptable concessions:

**Security Scanning**:
- May support language-specific scanners (e.g., npm audit, Snyk)
- Always optional, never required

**Default Worker Images**:
- Ubuntu LTS chosen for broad compatibility
- Does not preclude custom Docker images

**Package Registry**:
- Support ecosystems as they gain mainstream adoption
- Prioritize based on organizational usage, not personal preference

### Language Adoption Process

When teams want a new language/framework:

1. **No Permission Required**: Teams can use any language immediately
2. **CI/CD Workflow**: Team writes `setup-<language>` steps
3. **Package Registry**: If needed, request Nexus repository (standard process)
4. **Share Examples**: Optionally contribute template to help others

### Monitoring Language Diversity

Track (but do not restrict) language usage to understand platform effectiveness:
- Count projects by primary language (via `.gitattributes` or repository metadata)
- Monitor CI/CD workflow diversity
- Identify underserved ecosystems for potential registry additions

### Polyglot Project Example

```yaml
# Monorepo with backend (Go), frontend (React), and infra (Terraform)
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-go@v3
        with:
          go-version: '1.21'
      - run: cd backend && go test ./...
  
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci && npm test
  
  infrastructure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: '1.6'
      - run: cd infra && terraform validate
```

### Décisions Connexes

- [ADR-0002 : Scalabilité Actions](0002-scalabilite-actions.md) — Architecture runner générique permet neutralité
- [ADR-0004 : Plugins MVP](0004-plugins-mvp.md) — Registry packages supporte écosystèmes multiples
- [ADR-0007 : Intégration Nexus](0007-integration-nexus.md) — Nexus choisi pour support multi-écosystème

### Références

- GitHub Actions Environments : https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners
- Polyglot Programming : https://en.wikipedia.org/wiki/Polyglot_(computing)
- Inventaire technologique interne (Confluence : "Tech Stack Inventory")
