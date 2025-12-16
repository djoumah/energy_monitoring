"""Tests unitaires pour le module sensors."""
import pytest
from src.sensors.iot_sensor import IoTSensor, SensorNetwork


class TestIoTSensor:
    """Tests pour la classe IoTSensor."""

    def test_sensor_initialization(self):
        """Test l'initialisation d'un capteur."""
        sensor = IoTSensor("TEST_001", "Bureau", 100.0, 20.0)
        assert sensor.sensor_id == "TEST_001"
        assert sensor.location == "Bureau"
        assert sensor.base_consumption == 100.0
        assert sensor.variance == 20.0
        assert sensor.is_active is True

    def test_read_consumption_active(self):
        """Test la lecture d'un capteur actif."""
        sensor = IoTSensor("TEST_001", "Bureau", 100.0, 20.0)
        reading = sensor.read_consumption()
        assert reading is not None
        assert 'sensor_id' in reading
        assert 'consumption_kwh' in reading
        assert reading['consumption_kwh'] > 0

    def test_read_consumption_inactive(self):
        """Test la lecture d'un capteur inactif."""
        sensor = IoTSensor("TEST_001", "Bureau", 100.0, 20.0)
        sensor.deactivate()
        reading = sensor.read_consumption()
        assert reading is None


class TestSensorNetwork:
    """Tests pour la classe SensorNetwork."""

    def test_add_sensor(self):
        """Test l'ajout d'un capteur."""
        network = SensorNetwork()
        sensor = IoTSensor("TEST_001", "Bureau", 100.0, 20.0)
        network.add_sensor(sensor)
        assert len(network.sensors) == 1

    def test_read_all_sensors(self):
        """Test la lecture de tous les capteurs."""
        network = SensorNetwork()
        sensor1 = IoTSensor("TEST_001", "Bureau", 100.0, 20.0)
        sensor2 = IoTSensor("TEST_002", "Entrepôt", 200.0, 30.0)
        network.add_sensor(sensor1)
        network.add_sensor(sensor2)
        measurements = network.read_all_sensors()
        assert len(measurements) == 2
