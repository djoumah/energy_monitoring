"""
Module de gestion du stockage MongoDB pour les données énergétiques.
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from typing import List, Dict, Optional
from datetime import datetime


class MongoDBHandler:
    """Gestionnaire de base de données MongoDB."""

    def __init__(self, connection_string: str = "mongodb://localhost:27017/",
                 database_name: str = "energy_monitoring"):
        """
        Initialise la connexion MongoDB.

        Args:
            connection_string: URL de connexion MongoDB
            database_name: Nom de la base de données
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self) -> bool:
        """
        Établit la connexion à MongoDB.

        Returns:
            True si connexion réussie, False sinon
        """
        try:
            self.client = MongoClient(self.connection_string,
                                      serverSelectionTimeoutMS=5000)
            # Test de connexion
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.collection = self.db['measurements']
            return True
        except ConnectionFailure as e:
            print(f"Erreur de connexion MongoDB: {e}")
            return False

    def disconnect(self):
        """Ferme la connexion MongoDB."""
        if self.client:
            self.client.close()

    def insert_measurement(self, measurement: Dict) -> Optional[str]:
        """
        Insère une mesure dans la base.

        Args:
            measurement: Dictionnaire contenant les données de mesure

        Returns:
            ID du document inséré ou None
        """
        try:
            result = self.collection.insert_one(measurement)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Erreur d'insertion: {e}")
            return None

    def insert_measurements(self, measurements: List[Dict]) -> int:
        """
        Insère plusieurs mesures dans la base.

        Args:
            measurements: Liste de mesures

        Returns:
            Nombre de documents insérés
        """
        if not measurements:
            return 0

        try:
            result = self.collection.insert_many(measurements)
            return len(result.inserted_ids)
        except PyMongoError as e:
            print(f"Erreur d'insertion multiple: {e}")
            return 0

    def get_measurements(self, sensor_id: Optional[str] = None,
                         limit: int = 100) -> List[Dict]:
        """
        Récupère les mesures de la base.

        Args:
            sensor_id: Filtrer par ID de capteur (optionnel)
            limit: Nombre maximum de résultats

        Returns:
            Liste des mesures
        """
        try:
            query = {'sensor_id': sensor_id} if sensor_id else {}
            cursor = self.collection.find(query).sort(
                'timestamp', -1
            ).limit(limit)
            return list(cursor)
        except PyMongoError as e:
            print(f"Erreur de lecture: {e}")
            return []

    def get_recent_measurements(self, hours: int = 24) -> List[Dict]:
        """
        Récupère les mesures récentes.

        Args:
            hours: Nombre d'heures à remonter

        Returns:
            Liste des mesures récentes
        """
        try:
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(hours=hours)
            query = {'timestamp': {'$gte': cutoff_time}}
            cursor = self.collection.find(query).sort('timestamp', -1)
            return list(cursor)
        except PyMongoError as e:
            print(f"Erreur de lecture: {e}")
            return []

    def get_statistics(self, sensor_id: str) -> Optional[Dict]:
        """
        Calcule les statistiques pour un capteur.

        Args:
            sensor_id: Identifiant du capteur

        Returns:
            Dictionnaire de statistiques
        """
        try:
            pipeline = [
                {'$match': {'sensor_id': sensor_id}},
                {'$group': {
                    '_id': '$sensor_id',
                    'avg_consumption': {'$avg': '$consumption_kwh'},
                    'max_consumption': {'$max': '$consumption_kwh'},
                    'min_consumption': {'$min': '$consumption_kwh'},
                    'count': {'$sum': 1}
                }}
            ]
            result = list(self.collection.aggregate(pipeline))
            return result[0] if result else None
        except PyMongoError as e:
            print(f"Erreur de calcul des statistiques: {e}")
            return None

    def clear_collection(self):
        """Supprime toutes les données de la collection."""
        try:
            self.collection.delete_many({})
        except PyMongoError as e:
            print(f"Erreur de suppression: {e}")
