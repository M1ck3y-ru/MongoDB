# MongoDB Replica Set & Application Integration

Ce projet démontre l'utilisation de MongoDB en mode replica set et son intégration dans une application Python. Il est divisé en plusieurs parties qui couvrent différents aspects de MongoDB.

## Partie 2 - MongoDB Replica Set

Cette section concerne la configuration et l'utilisation d'un cluster MongoDB en replica set.

### Configuration des membres du replica set

Un replica set à 3 nœuds a été déployé via Docker Compose:
- **mongo1**: Nœud primaire (PRIMARY)
- **mongo2**: Nœud secondaire (SECONDARY)
- **mongo3**: Nœud secondaire (SECONDARY)

Les ports exposés sont:
- mongo1: 27018
- mongo2: 27019
- mongo3: 27020

### Méthodes d'initialisation

Le replica set a été initialisé en utilisant les méthodes suivantes:

```javascript
// Initialisation de base
rs.initiate()

// Ajout des autres membres
rs.add("mongo2:27017")
rs.add("mongo3:27017")
```

Alternativement, on peut initialiser avec une configuration complète:

```javascript
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
```

Le statut du replica set peut être vérifié avec:

```javascript
rs.status()
```

### Connexions possibles

Différentes URI de connexion peuvent être utilisées selon les besoins:

1. Connexion de base au replica set:
```
mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0
```

2. Connexion avec authentification:
```
mongodb://root:password@mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0
```

3. Connexion avec préférence de lecture:
```
mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0&readPreference=secondary
```

### Modes de lecture/écriture

- **Écriture**: Uniquement possible sur le nœud PRIMARY
- **Lecture**: Par défaut sur le PRIMARY, mais peut être configurée pour les SECONDARY

Pour activer la lecture sur un nœud SECONDARY:
```javascript
rs.secondaryOk()
// ou
db.getMongo().setReadPref("secondaryPreferred")
```

Options de préférence de lecture:
- `primary`: Lecture uniquement sur le PRIMARY (défaut)
- `primaryPreferred`: Préfère le PRIMARY, utilise un SECONDARY si nécessaire
- `secondary`: Lecture uniquement sur les SECONDARY
- `secondaryPreferred`: Préfère les SECONDARY, utilise le PRIMARY si nécessaire
- `nearest`: Lecture sur le nœud avec la latence la plus faible

## Partie 3 - Intégration dans une application

Cette section présente une application Python qui se connecte à MongoDB et effectue diverses opérations.

### Dépendances

```
pymongo
```

Installation: `pip install pymongo`

### Code de connexion

```python
def connect_to_mongodb():
    # URI de connexion avec authentification pour replica set
    uri = "mongodb://root:password@localhost:27018,localhost:27019,localhost:27020/?replicaSet=rs0"
    
    # Créer une connexion au cluster MongoDB
    client = MongoClient(uri)
    return client
```

L'URI expliquée:
- `mongodb://`: Protocole
- `root:password@`: Identifiants d'authentification
- `localhost:27018,localhost:27019,localhost:27020`: Adresses des serveurs
- `/?replicaSet=rs0`: Paramètre indiquant le nom du replica set
- Options additionnelles possibles: `readPreference`, `authSource`, etc.

### Opérations réalisées

L'application implémente toutes les opérations CRUD:
- CREATE: Insertion de documents uniques et multiples
- READ: Requêtes avec filtres
- UPDATE: Mise à jour de documents
- DELETE: Suppression de documents

### Résultats des tests

Les tests ont montré:
- La capacité à se connecter au replica set
- L'exécution réussie de toutes les opérations CRUD
- Le basculement automatique en cas d'indisponibilité du nœud primaire

## Utilisation

1. Démarrer le replica set:
```bash
docker-compose up -d
```

2. Initialiser le replica set:
```bash
docker exec -it mongo1 mongosh
```
```javascript
rs.initiate()
rs.add("mongo2:27017")
rs.add("mongo3:27017")
```

3. Exécuter l'application Python:
```bash
python mongodb_app.py
```

## Notes additionnelles

Pour une utilisation en production, considérez:
- L'utilisation de certificats SSL pour la connexion sécurisée
- La mise en place d'une stratégie de sauvegarde
- La configuration de la journalisation avancée
- L'optimisation des performances via des index appropriés
