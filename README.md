# Mini projet 
# Système de Suivi et Analyse de la Consommation Énergétique

## 📋 Description

Ce projet simule un dispositif de suivi et d'analyse de la consommation énergétique basé sur des capteurs IoT.

## 🚀 Installation

### Prérequis
- Python 3.8+
- MongoDB 4.4+

### Étapes


# 1. Telecharger le depot 
puis extraire les fichiers sur votre pc 


# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Démarrer MongoDB
# Linux/Mac
sudo systemctl start mongod

# Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## 💻 Utilisation

```bash
python main.py
```

## 🧪 Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=src --cov-report=html
```

## 🔍 Qualité du code

```bash
flake8 src/ tests/ main.py
```

## 📊 Fonctionnalités

- ✅ Simulation de capteurs IoT
- ✅ Stockage MongoDB
- ✅ Détection d'anomalies statistique
- ✅ Tests unitaires complets
- ✅ Code respectant PEP8

## 📄 Licence

UMMTO PHD  License
"#  Mini Projet energy_monitoring" 
