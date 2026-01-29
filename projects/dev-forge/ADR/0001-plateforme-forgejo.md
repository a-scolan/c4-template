# ADR-0001 : Sélection de la Plateforme Forgejo

## Statut

Accepté

## Contexte

Dev-Forge nécessite une plateforme Git auto-hébergée qui fournit :
- Hébergement et gestion Git (exigence fondamentale)
- Capacités d'automatisation CI/CD
- Outils de revue de code et de collaboration
- Déploiement on-premises (exigence organisationnelle)
- Intégration registry de packages
- Support techno-agnostique (tout langage/framework)
- Empreinte ressource raisonnable
- Développement actif et communauté

### Alternatives Considérées

**GitLab Community Edition** :
- ✅ Plateforme riche en fonctionnalités, mature
- ✅ CI/CD solide (GitLab CI)
- ✅ Registry de containers intégré
- ❌ Exigences en ressources lourdes (8 GB RAM minimum)
- ❌ Architecture complexe (services multiples)
- ❌ **⚠️ CRITIQUE : Procédures de maintenance et mise à jour complexes** - Mises à niveau multi-étapes nécessitant un séquençage de versions soigneux, migrations de base de données manuelles, orchestration de services entre composants multiples, et fenêtres de temps d'arrêt significatives. Cette charge opérationnelle crée un risque inacceptable pour notre environnement on-premises.
- ❌ Performances lentes sur matériel modeste
- ❌ Limitations Community Edition (certaines fonctionnalités Enterprise uniquement)

**Gitea** :
- ✅ Léger, performances rapides
- ✅ Déploiement simple (binaire unique)
- ✅ Exigences en ressources faibles
- ✅ UI/UX similaire à GitHub
- ⚠️ CI/CD limité (Gitea Actions émergent)
- ⚠️ Communauté plus petite que GitLab
- Note : Forgejo est un soft fork de Gitea

**GitHub Enterprise Server** :
- ✅ Standard de l'industrie, familier aux développeurs
- ✅ Excellent CI/CD Actions
- ✅ Meilleure expérience de revue de code
- ❌ Propriétaire, closed-source
- ❌ Licence coûteuse
- ❌ Nécessite connectivité Internet constante pour mises à jour
- ❌ Options de personnalisation limitées

**BitBucket Server/Data Center** :
- ✅ Intégration Atlassian (Jira, Confluence)
- ✅ Revue de code mature (pull requests)
- ❌ Licence Atlassian coûteuse
- ❌ Basé Java (utilisation ressources plus élevée)
- ❌ CI/CD nécessite installation Bamboo séparée
- ❌ Communauté open-source moins active

### Matrice des Exigences Clés

| Exigence | GitLab CE | Gitea | Forgejo | GitHub Ent | BitBucket |
|----------|-----------|-------|---------|------------|-----------|
| On-premises | ✅ | ✅ | ✅ | ✅ | ✅ |
| Open source | ✅ | ✅ | ✅ | ❌ | ❌ |
| Léger | ❌ | ✅ | ✅ | ❌ | ❌ |
| CI/CD natif | ✅ | ⚠️ | ✅ | ✅ | ❌ |
| Dév actif | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Coût | Gratuit | Gratuit | Gratuit | $$$$ | $$$$ |

## Décision

Nous adopterons **Forgejo** comme plateforme Git de Dev-Forge.

### Justification

1. **Déjà Utilisé** : Les équipes organisationnelles connaissent Forgejo, réduisant la charge de formation

2. **Efficacité Ressources** : Fonctionne bien sur matériel modeste (2 GB RAM, 2 vCPU), permettant un scaling rentable

3. **CI/CD Intégré** : Forgejo Actions fournit des workflows compatibles GitHub Actions sans outillage additionnel

4. **Gouvernance Open Source** : Fork piloté par la communauté assure transparence et évite le vendor lock-in

5. **Développement Actif** : Releases régulières, mainteneurs réactifs, écosystème en croissance

6. **Chemin de Migration** : Compatible avec Gitea, fournit chemin de mise à niveau si nécessaire

7. **Neutralité Technologique** : Aucun biais langage/framework—supporte tous les écosystèmes également

### Pourquoi Pas les Autres

**GitLab** : Surcharge en ressources (8+ GB RAM) incompatible avec le budget d'infrastructure cible. **Plus critique encore**, les procédures de maintenance et mise à jour complexes de GitLab—nécessitant séquençage de versions soigneux, migrations multi-étapes, changements de schéma de base de données, et redémarrages de services coordonnés—créent une charge opérationnelle et un risque inacceptables pour notre déploiement on-premises. Une seule mise à niveau ratée peut résulter en heures de temps d'arrêt et perte potentielle de données.

**Gitea** : Forgejo offre les mêmes bénéfices plus un engagement plus fort envers la gouvernance open-source

**GitHub Enterprise** : Licence propriétaire et coûts injustifiés pour le cas d'usage on-premises

## Conséquences

### Conséquences Positives

- **Interface Familière** : Équipes déjà expérimentées avec UI/workflows Forgejo
- **Performances Rapides** : Binaire Go léger assure expérience réactive
- **Opérations Simples** : Binaire unique simplifie déploiement, mises à jour et débogage
- **Rentable** : Pas de coûts de licence, exigences d'infrastructure modestes
- **Piloté par la Communauté** : Modèle de gouvernance ouverte s'aligne avec les valeurs organisationnelles
- **Compatibilité Actions** : Peut exploiter la connaissance et workflows GitHub Actions existants
- **À l'épreuve du futur** : Développement communautaire actif assure améliorations continues

### Conséquences Négatives

- **Écosystème Plus Petit** : Moins d'intégrations et plugins comparé à GitLab ou GitHub
- **Maturité Features** : Certaines fonctionnalités avancées moins matures que les équivalents GitLab
- **Taille Communauté** : Communauté plus petite signifie moins de réponses Stack Overflow/tutoriels
- **Support Commercial** : Options de support payé limitées comparé aux plateformes enterprise
- **Perception** : Marque moins reconnue comparé à GitHub/GitLab

### Conséquences Neutres

- **Dynamique Soft Fork** : Doit surveiller la relation Gitea/Forgejo pour divergence potentielle
- **Courbe d'Apprentissage** : Nouveaux développeurs non familiers avec Forgejo nécessitent onboarding (atténué par similarité avec GitHub)
- **Travail d'Intégration** : Peut nécessiter intégrations personnalisées pour outils organisationnels

## Notes

### Considérations de Migration

Forgejo supporte l'import depuis :
- GitHub (dépôts, issues, pull requests)
- GitLab
- Gitea
- Dépôts Git génériques

Ceci permet une migration graduelle des dépôts existants si nécessaire.

### Décisions connexes

- [ADR-0002 : Scalabilité Actions](0002-scalabilite-actions.md) — Architecture runners CI/CD
- [ADR-0004 : Plugins MVP](0004-plugins-mvp.md) — Fonctionnalités essentielles de la plateforme

### Critères de Révision

Cette décision devrait être révisée si :
- Le développement communautaire stagne (pas de releases pendant 12+ mois)
- Problème de sécurité critique non patché pendant 6+ mois
- Les performances se dégradent significativement à l'échelle
- La divergence Gitea/Forgejo crée des problèmes de compatibilité significatifs

### Références

- Documentation Officielle Forgejo : https://forgejo.org/docs/
- Comparaison Forgejo vs Gitea : https://forgejo.org/compare-to-gitea/
- Exigences Système GitLab : https://docs.gitlab.com/ee/install/requirements.html
- Feedback équipe interne (Confluence : "Évaluation Plateforme Git")
