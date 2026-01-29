# ADR-0005 : Architecture des Zones Réseau

## Statut

Accepté

## Contexte

L'infrastructure Dev-Forge doit implémenter une sécurité en profondeur via la segmentation réseau. Cela isole les services, limite le rayon d'impact des incidents de sécurité, et applique l'accès réseau au moindre privilège.

**Exigences de Sécurité** :
- Pas d'accès Internet direct vers le tier application
- Tier base de données isolé des réseaux externes
- Règles firewall claires entre les zones
- Trafic réseau auditable et monitorable
- Alignement avec les politiques de sécurité organisationnelles

**Contexte Organisationnel** :
- Datacenter on-premises avec capacité VLAN
- Infrastructure firewall existante (firewalls matériels, groupes de sécurité)
- L'équipe réseau gère le provisioning VLAN
- L'équipe sécurité audite les règles firewall trimestriellement

**Services à Déployer** :
- Application web Forgejo (accès externe requis)
- Base de données PostgreSQL (interne uniquement)
- Runners Forgejo Actions (interne uniquement, doivent accéder à Forgejo et repos de packages externes)
- Reverse proxy/load balancer (face à Internet)

### Alternatives Considérées

**Réseau Plat (Pas de Segmentation)** :
- ✅ Configuration simple
- ✅ Pas de règles firewall à gérer
- ❌ **Viole la politique de sécurité**
- ❌ Un compromis unique cascade vers tous les services
- ❌ Ne permet pas d'auditer/limiter les flux de trafic
- ❌ Échec de conformité

**DMZ Uniquement (Deux-Tiers)** :
- ✅ Plus simple que trois-tiers
- ✅ Protège les services internes d'Internet
- ❌ Application et base de données dans même zone (privilège excessif)
- ❌ Les runners ont accès direct à la base de données (inutile)
- ❌ N'isole pas le traitement async

**Architecture Quatre+ Tiers** :
- ✅ Segmentation maximale
- ✅ Zones séparées pour traitement, données, monitoring, backup
- ❌ Trop complexe pour l'échelle Dev-Forge
- ❌ Surcharge de gestion (nombreuses règles firewall)
- ❌ Difficile de troubleshooter les problèmes de connectivité

**Groupes de Sécurité Style Cloud** (sans VLANs) :
- ✅ Contrôle fin, niveau service
- ✅ Fonctionne dans environnements cloud
- ❌ Nécessite SDN ou infrastructure cloud (pas disponible on-premises)
- ❌ Ajoute de la complexité sans valeur prouvée pour ce cas d'usage

## Décision

Nous implémenterons une **architecture réseau trois-tiers** avec des zones distinctes :

### Définitions des Zones

#### 1. DMZ (Zone Démilitarisée)
**Objectif** : Services edge face à Internet

**Services** :
- Reverse proxy / load balancer (HAProxy, Nginx, F5)
- Terminaison TLS
- Limitation de taux et WAF (si applicable)

**Réseau** : 
- VLAN 100 : `10.0.100.0/24`
- Passerelle : `10.0.100.1`

**Règles Firewall** :
- **Entrant** : HTTPS (443) depuis Internet
- **Sortant** : HTTPS (443, 3000) vers AppTier uniquement
- **Bloqué** : Accès direct vers DataTier, ProcTier

**Caractéristiques** :
- Surface de service minimale
- Pas de données sensibles stockées
- Configurations OS durcies
- Mises à jour de sécurité fréquentes

#### 2. AppTier (Tier Application)
**Objectif** : Logique applicative et services

**Services** :
- Application web Forgejo
- Backend API Forgejo
- Scheduler Forgejo Actions

**Réseau** :
- VLAN 101 : `10.1.0.0/24`
- Passerelle : `10.1.0.1`

**Règles Firewall** :
- **Entrant** : HTTPS (3000) depuis DMZ uniquement
- **Sortant** : 
  - PostgreSQL (5432) vers DataTier
  - HTTP/HTTPS pour repos de packages externes (pour Actions)
- **Bloqué** : Internet entrant direct, accès direct aux containers runners

**Caractéristiques** :
- Stateless si possible (permet scaling horizontal)
- Secrets accédés via Hiera/Puppet (pas stockés dans configs)
- Health checks exposés sur interface de gestion

#### 3. DataTier (Tier Données/Persistance)
**Objectif** : Stockage de données et état persistant

**Services** :
- Base de données PostgreSQL
- Stockage fichiers (dépôts Git, LFS)
- (Futur : stockage backup)

**Réseau** :
- VLAN 102 : `10.2.0.0/24`
- Passerelle : `10.2.0.1`

**Règles Firewall** :
- **Entrant** : PostgreSQL (5432) depuis AppTier uniquement
- **Sortant** : Aucun (isolé sauf pour backups)
- **Bloqué** : Tout autre trafic

**Caractéristiques** :
- Pas d'accès Internet sortant
- Chiffré au repos (LUKS ou équivalent)
- Backups quotidiens vers réseau/stockage séparé

### Diagramme de Flux de Trafic

```
Internet
    ↓ HTTPS (443)
┌─────────────┐
│DMZ          │ VLAN 100
│Load Balancer│
└─────────────┘
    ↓ HTTPS (3000)
┌─────────────┐
│AppTier      │ VLAN 101
│Forgejo + Runners
└─────────────┘
    ↓ PostgreSQL (5432)
┌─────────────┐
│DataTier     │ VLAN 102
│PostgreSQL   │
└─────────────┘
  (pas de sortant)
```

### Placement des Runners

**Les runners Forgejo Actions** sont dans AppTier :
- Besoin d'accès à l'API Forgejo (même VLAN)
- Besoin d'Internet sortant pour téléchargements de dépendances (npm, PyPI, Maven)
- N'ont PAS besoin d'accès direct à la base de données
- Containers éphémères (rayon d'impact limité)

## Conséquences

### Conséquences Positives

- **Défense en Profondeur** : Frontières de sécurité multiples—compromis dans une zone ne cascade pas
- **Moindre Privilège** : Chaque zone accède uniquement à ce dont elle a besoin (la base de données ne touche jamais Internet)
- **Auditabilité** : Les flux de trafic sont explicites et journalisables aux frontières de zone
- **Conformité** : Rencontre les standards de sécurité organisationnels pour la segmentation réseau
- **Confinement d'Incident** : Un runner compromis ne peut pas accéder directement à la base de données
- **Responsabilités Claires** : L'équipe réseau gère les zones, l'équipe app gère les services

### Conséquences Négatives

- **Complexité** : Trois VLANs à gérer, règles firewall à maintenir
- **Troubleshooting** : Problèmes réseau plus difficiles à diagnostiquer à travers les frontières de zone
- **Dépendance Firewall** : Règle mal configurée peut casser la connectivité
- **Processus de Changement** : Changements firewall nécessitent coordination avec l'équipe réseau
- **Surcharge de Test** : Doit tester la connectivité entre toutes les zones pendant le déploiement

### Conséquences Neutres

- **Placement Monitoring** : Les agents de monitoring ont besoin de règles firewall pour atteindre les endpoints de métriques
- **Stratégie de Backup** : Les backups doivent traverser les frontières de zone (nécessite règle firewall)
- **Scaling Futur** : Les services additionnels doivent être classés dans des zones

## Notes

### Directives d'Assignation de Zone

**DMZ** : Uniquement les services qui DOIVENT être accessibles depuis Internet
**AppTier** : Logique applicative qui doit communiquer avec zones multiples
**DataTier** : Tout ce qui stocke des données persistantes et sensibles

### Gestion des Règles Firewall

**Convention de Nommage des Règles** :
```
<zone-source>-to-<zone-dest>-<protocole>-<but>
Exemple : AppTier-to-DataTier-tcp-postgres
```

**Documentation des Règles** :
- Chaque règle doit avoir un commentaire expliquant le but métier
- Règles révisées trimestriellement (exigence équipe sécurité)
- Règles inutilisées retirées après 90 jours

### Staging vs Production

**Architecture de zone identique** mais VLANs séparés :

| Zone | VLAN Staging | VLAN Production |
| AppTier | 101 (10.1.0.0/24) | 201 (10.1.0.0/24) |
| DataTier | 102 (10.2.0.0/24) | 202 (10.2.0.0/24) |

### Zones Futures (Déférées)

**ProcTier (Tier Traitement)** :
- Si le traitement async a besoin d'isolation plus forte du tier application
- Se situerait entre AppTier et DataTier
- Pour queues de messages, workers background, traitement par lots

**SecZone (Zone Sécurité/Monitoring)** :
- Zone dédiée pour monitoring, logging, scanning de sécurité
- Réseau latéral pour health checks
- Déféré jusqu'à maturité des exigences de monitoring

### Accès d'Urgence

**Procédure break-glass** :
- Hôte bastion SSH dans DMZ (IP source restreinte, MFA requis)
- Règles firewall temporaires avec expiration automatique (4 heures)
- Tous les accès d'urgence journalisés et audités

### Décisions connexes

- [ADR-0003 : Automatisation Puppet](0003-automatisation-puppet.md) — Puppet applique la configuration de zone
- [ADR-0002 : Scalabilité Actions](0002-scalabilite-actions.md) — Runners placés dans AppTier

### Références

- Meilleures Pratiques de Segmentation Réseau : NIST SP 800-82
- Politique de Sécurité Réseau Organisationnelle (Confluence : "Sécurité/Réseau")
- Processus de Demande de Changement Firewall (ServiceNow : "Modèle CR Firewall")
