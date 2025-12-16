"""
Module de simulation des capteurs IoT pour la consommation énergétique.
"""
import random
from datetime import datetime
from typing import Dict, Optional


class IoTSensor:
    """Classe représentant un capteur IoT simulé."""

    def __init__(self, sensor_id: str, location: str,
                 base_consumption: float = 100.0,
                 variance: float = 20.0):
        """
        Initialise un capteur IoT.

        Args:
            sensor_id: Identifiant unique du capteur
            location: Localisation du capteur
            base_consumption: Consommation de base en kWh
            variance: Variance de la consommation
        """
        self.sensor_id = sensor_id
        self.location = location
        self.base_consumption = base_consumption
        self.variance = variance
        self.is_active = True

    def read_consumption(self) -> Optional[Dict]:
        """
        Génère une lecture de consommation énergétique.

        Returns:
            Dictionnaire contenant les données de mesure
        """
        if not self.is_active:
            return None

        # Génération de la consommation avec variation aléatoire
        consumption = self.base_consumption + random.uniform(
            -self.variance, self.variance
        )

        # Simulation d'anomalies occasionnelles (5% de chance)
        if random.random() < 0.05:
            consumption *= random.uniform(2.0, 3.0)

        measurement = {
            'sensor_id': self.sensor_id,
            'location': self.location,
            'consumption_kwh': round(consumption, 2),
            'timestamp': datetime.now(),
            'status': 'active'
        }

        return measurement

    def deactivate(self):
        """Désactive le capteur."""
        self.is_active = False

    def activate(self):
        """Active le capteur."""
        self.is_active = True


class SensorNetwork:
    """Gestion d'un réseau de capteurs IoT."""

    def __init__(self):
        """Initialise le réseau de capteurs."""
        self.sensors = {}

    def add_sensor(self, sensor: IoTSensor):
        """
        Ajoute un capteur au réseau.

        Args:
            sensor: Instance de IoTSensor à ajouter
        """
        self.sensors[sensor.sensor_id] = sensor

    def remove_sensor(self, sensor_id: str):
        """
        Retire un capteur du réseau.

        Args:
            sensor_id: Identifiant du capteur à retirer
        """
        if sensor_id in self.sensors:
            del self.sensors[sensor_id]

    def read_all_sensors(self) -> list:
        """
        Lit tous les capteurs actifs.

        Returns:
            Liste des mesures de tous les capteurs
        """
        measurements = []
        for sensor in self.sensors.values():
            reading = sensor.read_consumption()
            if reading:
                measurements.append(reading)
        return measurements

    def get_sensor(self, sensor_id: str) -> Optional[IoTSensor]:
        """
        Récupère un capteur spécifique.

        Args:
            sensor_id: Identifiant du capteur

        Returns:
            Instance du capteur ou None
        """
        return self.sensors.get(sensor_id)
