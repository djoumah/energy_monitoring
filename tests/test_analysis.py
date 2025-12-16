"""Tests unitaires pour le module d'analyse."""
import pytest
from datetime import datetime
from src.analysis.anomaly_detector import AnomalyDetector


class TestAnomalyDetector:
    """Tests pour la classe AnomalyDetector."""

    def test_detector_initialization(self):
        """Test l'initialisation du détecteur."""
        detector = AnomalyDetector(threshold_multiplier=2.0)
        assert detector.threshold_multiplier == 2.0
        assert len(detector.baseline_stats) == 0

    def test_calculate_baseline(self):
        """Test le calcul de la baseline."""
        detector = AnomalyDetector()
        measurements = [
            {'sensor_id': 'TEST_001', 'consumption_kwh': 100.0,
             'timestamp': datetime.now()},
            {'sensor_id': 'TEST_001', 'consumption_kwh': 110.0,
             'timestamp': datetime.now()},
            {'sensor_id': 'TEST_001', 'consumption_kwh': 90.0,
             'timestamp': datetime.now()},
        ]
        detector.calculate_baseline(measurements, 'TEST_001')
        baseline = detector.get_sensor_baseline('TEST_001')
        assert baseline is not None
        assert 'mean' in baseline

    def test_detect_high_anomaly(self):
        """Test la détection d'une anomalie haute."""
        detector = AnomalyDetector(threshold_multiplier=1.5)
        measurements = [
            {'sensor_id': 'TEST_001', 'consumption_kwh': 100.0,
             'timestamp': datetime.now()}
            for _ in range(10)
        ]
        detector.calculate_baseline(measurements, 'TEST_001')
        test_measurement = {
            'sensor_id': 'TEST_001',
            'consumption_kwh': 200.0,
            'timestamp': datetime.now()
        }
        anomaly = detector.detect_anomaly(test_measurement)
        assert anomaly is not None
        assert anomaly['type'] == 'HIGH'
