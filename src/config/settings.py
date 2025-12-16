"""
Configuration globale du projet.
"""

# Configuration MongoDB
MONGODB_CONFIG = {
    'connection_string': 'mongodb://localhost:27017/',
    'database_name': 'energy_monitoring',
    'collection_name': 'measurements'
}

# Configuration des capteurs
SENSOR_CONFIG = {
    'default_base_consumption': 100.0,
    'default_variance': 20.0,
    'anomaly_probability': 0.05,
    'reading_interval': 0.5
}

# Configuration de la détection d'anomalies
ANOMALY_CONFIG = {
    'threshold_multiplier': 2.0,
    'baseline_samples': 20,
    'monitoring_cycles': 30
}

# Configuration des tests
TEST_CONFIG = {
    'test_database': 'energy_monitoring_test',
    'mock_mongodb': True
}

# Logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'energy_monitoring.log'
}
