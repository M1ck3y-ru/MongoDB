# Pour ce fichier nous avons utiliser Claude sonnet pour la génération du fichier et mieux comprendre les fonctions
from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
import datetime
import pprint

# Fonction de connexion à MongoDB
def connect_to_mongodb():
    """
    Se connecte à MongoDB en utilisant une URI qui spécifie le replica set
    """
    # URI de connexion avec authentification
    # Format: mongodb://utilisateur:motdepasse@hôte1:port1,hôte2:port2,hôte3:port3/?replicaSet=nom&options
    uri = "mongodb://root:le_bras_sur_la_chaise238@localhost:27018,localhost:27019,localhost:27020/?replicaSet=rs0"
    
    # Créer une connexion au cluster MongoDB
    client = MongoClient(uri)
    
    # Vérifier la connexion
    try:
        # La méthode server_info() vérifie si le serveur est accessible
        server_info = client.server_info()
        print(f"Connexion réussie à MongoDB version {server_info.get('version')}")
        return client
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return None

# Opérations CRUD (Create, Read, Update, Delete)
def run_crud_operations(client):
    """
    Exécute les opérations CRUD de base sur MongoDB
    """
    # Sélection de la base de données et de la collection
    db = client.testdb
    collection = db.users
    
    # 1. CREATE: Insertion d'un document
    print("\n--- INSERTION ---")
    new_user = {
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com",
        "age": 30,
        "created_at": datetime.datetime.now()
    }
    result = collection.insert_one(new_user)
    print(f"Document inséré avec ID: {result.inserted_id}")
    
    # Insertion de plusieurs documents
    users = [
        {"name": "Marie Martin", "email": "marie.martin@example.com", "age": 25},
        {"name": "Pierre Durand", "email": "pierre.durand@example.com", "age": 35},
        {"name": "Sophie Lefevre", "email": "sophie.lefevre@example.com", "age": 28}
    ]
    result = collection.insert_many(users)
    print(f"Documents insérés avec IDs: {result.inserted_ids}")
    
    # 2. READ: Requêtes simples avec filtres
    print("\n--- LECTURE ---")
    # Trouver un document spécifique
    user = collection.find_one({"name": "Jean Dupont"})
    print("Utilisateur trouvé:")
    pprint.pprint(user)
    
    # Requête avec filtre
    print("\nUtilisateurs de moins de 30 ans:")
    for user in collection.find({"age": {"$lt": 30}}):
        pprint.pprint(user)
    
    # 3. UPDATE: Mise à jour d'un document
    print("\n--- MISE À JOUR ---")
    result = collection.update_one(
        {"name": "Jean Dupont"},
        {"$set": {"age": 31, "updated_at": datetime.datetime.now()}}
    )
    print(f"Documents modifiés: {result.modified_count}")
    
    # Vérifier la mise à jour
    user = collection.find_one({"name": "Jean Dupont"})
    print("Utilisateur après mise à jour:")
    pprint.pprint(user)
    
    # 4. DELETE: Suppression d'un document
    print("\n--- SUPPRESSION ---")
    result = collection.delete_one({"name": "Marie Martin"})
    print(f"Documents supprimés: {result.deleted_count}")
    
    # Requête après suppression
    count = collection.count_documents({})
    print(f"Nombre total d'utilisateurs restants: {count}")

# Démonstration des méthodes de connexion alternatives
def connection_methods():
    """
    Démonstration des différentes méthodes de connexion selon les cas d'utilisation
    """
    print("\n--- MÉTHODES DE CONNEXION ---")
    
    # 1. Connexion à un nœud standalone
    print("Connexion à un nœud standalone:")
    uri_standalone = "mongodb://localhost:27018"
    print(uri_standalone)
    
    # 2. Connexion à un replica set
    print("\nConnexion à un replica set:")
    uri_replicaset = "mongodb://localhost:27018,localhost:27019,localhost:27020/?replicaSet=rs0"
    print(uri_replicaset)
    
    # 3. Connexion sécurisée avec authentification
    print("\nConnexion sécurisée avec authentification:")
    uri_secure = "mongodb://root:password@localhost:27018,localhost:27019,localhost:27020/?replicaSet=rs0&authSource=admin"
    print(uri_secure)
    
    # 4. Connexion avec préférence de lecture (sur secondaires)
    print("\nConnexion avec préférence de lecture sur secondaires:")
    uri_secondary = "mongodb://localhost:27018,localhost:27019,localhost:27020/?replicaSet=rs0&readPreference=secondary"
    print(uri_secondary)

# Programme principal
if __name__ == "__main__":
    # Se connecter à MongoDB
    client = connect_to_mongodb()
    
    if client:
        # Exécuter les opérations CRUD
        run_crud_operations(client)
        
        # Démontrer les différentes méthodes de connexion
        connection_methods()
        
        # Fermer la connexion
        client.close()
        print("\nConnexion fermée.")