"""
Application principale de suivi de consommation énergétique.
"""
import time
from src.sensors.iot_sensor import IoTSensor, SensorNetwork
from src.storage.mongodb_handler import MongoDBHandler
from src.analysis.anomaly_detector import AnomalyDetector


def main():
    """Fonction principale de l'application."""
    print("=== Système de Suivi Énergétique ===\n")

    # Initialisation de MongoDB
    print("Connexion à MongoDB...")
    db_handler = MongoDBHandler()
    if not db_handler.connect():
        print("Impossible de se connecter à MongoDB. Vérifiez que MongoDB "
              "est en cours d'exécution.")
        return

    print("✓ Connecté à MongoDB\n")

    # Création du réseau de capteurs
    print("Initialisation des capteurs...")
    sensor_network = SensorNetwork()

    # Ajout de capteurs avec différentes caractéristiques
    sensors_config = [
        ("SENSOR_001", "Bureau Principal", 150.0, 30.0),
        ("SENSOR_002", "Entrepôt", 250.0, 50.0),
        ("SENSOR_003", "Salle Serveurs", 500.0, 75.0),
        ("SENSOR_004", "Cafétéria", 100.0, 20.0),
    ]

    for sensor_id, location, base, variance in sensors_config:
        sensor = IoTSensor(sensor_id, location, base, variance)
        sensor_network.add_sensor(sensor)
        print(f"✓ Capteur {sensor_id} ajouté ({location})")

    print()

    # Initialisation du détecteur d'anomalies
    anomaly_detector = AnomalyDetector(threshold_multiplier=2.0)

    # Phase 1: Collecte de données de référence
    print("Phase 1: Collecte des données de référence...")
    baseline_measurements = []

    for i in range(20):
        measurements = sensor_network.read_all_sensors()
        baseline_measurements.extend(measurements)
        db_handler.insert_measurements(measurements)
        time.sleep(0.1)

    print(f"✓ {len(baseline_measurements)} mesures collectées\n")

    # Calcul des baselines pour chaque capteur
    print("Calcul des baselines...")
    for sensor_id in sensor_network.sensors.keys():
        anomaly_detector.calculate_baseline(baseline_measurements, sensor_id)
        baseline = anomaly_detector.get_sensor_baseline(sensor_id)
        if baseline:
            print(f"✓ {sensor_id}: Moyenne = {baseline['mean']:.2f} kWh, "
                  f"Seuil = [{baseline['threshold_low']:.2f}, "
                  f"{baseline['threshold_high']:.2f}]")

    print()

    # Phase 2: Surveillance en temps réel
    print("Phase 2: Surveillance en temps réel (30 cycles)...")
    print("-" * 60)

    for cycle in range(30):
        measurements = sensor_network.read_all_sensors()
        db_handler.insert_measurements(measurements)

        # Détection d'anomalies
        anomalies = anomaly_detector.analyze_batch(measurements)

        if anomalies:
            for anomaly in anomalies:
                print(f"\n⚠ ANOMALIE DÉTECTÉE!")
                print(f"  Capteur: {anomaly['sensor_id']}")
                print(f"  Type: {anomaly['type']}")
                print(f"  Sévérité: {anomaly['severity']}")
                print(f"  Consommation: {anomaly['consumption']} kWh")
                print(f"  Plage attendue: "
                      f"{anomaly['expected_range'][0]:.2f} - "
                      f"{anomaly['expected_range'][1]:.2f} kWh")
        else:
            print(f"Cycle {cycle + 1}: Toutes les mesures normales")

        time.sleep(0.5)

    print("\n" + "-" * 60)

    # Affichage des statistiques finales
    print("\n=== Statistiques Finales ===\n")
    for sensor_id in sensor_network.sensors.keys():
        stats = db_handler.get_statistics(sensor_id)
        if stats:
            print(f"{sensor_id}:")
            print(f"  Nombre de mesures: {stats['count']}")
            print(f"  Consommation moyenne: {stats['avg_consumption']:.2f} "
                  f"kWh")
            print(f"  Min: {stats['min_consumption']:.2f} kWh")
            print(f"  Max: {stats['max_consumption']:.2f} kWh")
            print()

    # Nettoyage
    print("Fermeture des connexions...")
    db_handler.disconnect()
    print("✓ Terminé")


if __name__ == "__main__":
    main()
