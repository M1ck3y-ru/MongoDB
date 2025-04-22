"""
Script adapté à une configuration MongoDB avec noms d'hôtes mongo1, mongo2, mongo3
"""
from pymongo import MongoClient
import datetime
import pprint

def connect_to_mongodb():
    """
    Se connecte à MongoDB en utilisant les noms d'hôtes du replica set
    """
    try:
        # URI adaptée aux noms d'hôtes mongo1, mongo2, mongo3
        uri = "mongodb://root:le_bras_sur_la_chaise238@mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0"
        
        print(f"Tentative de connexion avec URI: {uri}")
        
        # Créer une connexion au cluster MongoDB
        client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        
        # Vérifier la connexion
        server_info = client.server_info()
        print(f"Connexion réussie à MongoDB version {server_info.get('version')}")
        return client
        
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return None

def run_basic_operations(client):
    """
    Exécute quelques opérations de base sur MongoDB
    """
    if not client:
        return
        
    try:
        # Sélection de la base de données et de la collection
        db = client.testdb
        collection = db.test_collection
        
        # Insertion d'un document
        print("\n--- INSERTION ---")
        new_doc = {
            "name": "Test Document",
            "created_at": datetime.datetime.now()
        }
        result = collection.insert_one(new_doc)
        print(f"Document inséré avec ID: {result.inserted_id}")
        
        # Lecture du document
        print("\n--- LECTURE ---")
        doc = collection.find_one({"name": "Test Document"})
        print("Document trouvé:")
        pprint.pprint(doc)
        
    except Exception as e:
        print(f"Erreur lors des opérations: {e}")
    
    finally:
        # Fermer la connexion
        client.close()
        print("\nConnexion fermée.")

if __name__ == "__main__":
    print("Démarrage du test de connexion MongoDB...")
    client = connect_to_mongodb()
    run_basic_operations(client)
    print("Test terminé.")