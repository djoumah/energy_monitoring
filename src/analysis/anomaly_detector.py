"""
Module de détection d'anomalies dans la consommation énergétique.
"""
import statistics
from typing import List, Dict, Optional


class AnomalyDetector:
    """Détecteur d'anomalies basé sur des méthodes statistiques."""

    def __init__(self, threshold_multiplier: float = 2.0):
        """
        Initialise le détecteur d'anomalies.

        Args:
            threshold_multiplier: Multiplicateur pour le seuil de détection
        """
        self.threshold_multiplier = threshold_multiplier
        self.baseline_stats = {}

    def calculate_baseline(self, measurements: List[Dict],
                           sensor_id: str):
        """
        Calcule les statistiques de base pour un capteur.

        Args:
            measurements: Liste des mesures historiques
            sensor_id: Identifiant du capteur
        """
        sensor_data = [
            m['consumption_kwh'] for m in measurements
            if m.get('sensor_id') == sensor_id
        ]

        if len(sensor_data) < 2:
            return

        mean = statistics.mean(sensor_data)
        stdev = statistics.stdev(sensor_data)

        self.baseline_stats[sensor_id] = {
            'mean': mean,
            'stdev': stdev,
            'threshold_high': mean + (self.threshold_multiplier * stdev),
            'threshold_low': max(0, mean - (self.threshold_multiplier * stdev))
        }

    def detect_anomaly(self, measurement: Dict) -> Optional[Dict]:
        """
        Détecte si une mesure est anormale.

        Args:
            measurement: Mesure à analyser

        Returns:
            Dictionnaire d'anomalie ou None si normale
        """
        sensor_id = measurement.get('sensor_id')
        consumption = measurement.get('consumption_kwh')

        if sensor_id not in self.baseline_stats:
            return None

        stats = self.baseline_stats[sensor_id]

        if consumption > stats['threshold_high']:
            return {
                'sensor_id': sensor_id,
                'timestamp': measurement['timestamp'],
                'consumption': consumption,
                'expected_range': (stats['threshold_low'],
                                   stats['threshold_high']),
                'type': 'HIGH',
                'severity': self._calculate_severity(
                    consumption, stats['threshold_high'], stats['mean']
                ),
                'message': f"Consommation élevée détectée: {consumption} kWh"
            }
        elif consumption < stats['threshold_low']:
            return {
                'sensor_id': sensor_id,
                'timestamp': measurement['timestamp'],
                'consumption': consumption,
                'expected_range': (stats['threshold_low'],
                                   stats['threshold_high']),
                'type': 'LOW',
                'severity': self._calculate_severity(
                    stats['threshold_low'], consumption, stats['mean']
                ),
                'message': f"Consommation faible détectée: {consumption} kWh"
            }

        return None

    def _calculate_severity(self, value: float, threshold: float,
                            mean: float) -> str:
        """
        Calcule la sévérité de l'anomalie.

        Args:
            value: Valeur mesurée
            threshold: Seuil de détection
            mean: Moyenne historique

        Returns:
            Niveau de sévérité (LOW, MEDIUM, HIGH, CRITICAL)
        """
        deviation = abs(value - mean) / mean

        if deviation > 2.0:
            return 'CRITICAL'
        elif deviation > 1.0:
            return 'HIGH'
        elif deviation > 0.5:
            return 'MEDIUM'
        else:
            return 'LOW'

    def analyze_batch(self, measurements: List[Dict]) -> List[Dict]:
        """
        Analyse un lot de mesures pour détecter les anomalies.

        Args:
            measurements: Liste de mesures à analyser

        Returns:
            Liste des anomalies détectées
        """
        anomalies = []
        for measurement in measurements:
            anomaly = self.detect_anomaly(measurement)
            if anomaly:
                anomalies.append(anomaly)
        return anomalies

    def get_sensor_baseline(self, sensor_id: str) -> Optional[Dict]:
        """
        Récupère les statistiques de base d'un capteur.

        Args:
            sensor_id: Identifiant du capteur

        Returns:
            Statistiques ou None
        """
        return self.baseline_stats.get(sensor_id)

    def update_baseline(self, sensor_id: str, measurements: List[Dict]):
        """
        Met à jour les statistiques de base d'un capteur.

        Args:
            sensor_id: Identifiant du capteur
            measurements: Nouvelles mesures
        """
        self.calculate_baseline(measurements, sensor_id)
