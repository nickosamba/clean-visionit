# CLEAN - Système de Gestion de Collecte de Déchets

CLEAN est une application de gestion complète pour les entreprises de collecte de déchets, permettant de gérer les clients, les abonnements, les agents de terrain, les zones géographiques (secteurs/rues), les paiements et les tournées de collecte.

## 🚀 Fonctionnalités

- **Tableau de Bord** : Vue d'ensemble pour les gestionnaires, comptables et agents.
- **Gestion des Clients** : Enregistrement, suivi des abonnements et géolocalisation.
- **Gestion des Agents** : Suivi des performances et assignation aux secteurs.
- **Zones & Secteurs** : Découpage géographique précis (Villes, Secteurs, Rues).
- **Abonnements & Services** : Gestion des forfaits et options de service.
- **Paiements** : Suivi des échéances et historique des règlements.
- **Tournées** : Planification et suivi des collectes sur le terrain.
- **Incidents** : Signalement et gestion des problèmes rencontrés lors des tournées.

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <url-du-depot>
cd config
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet en vous basant sur l'exemple suivant :
```env
SECRET_KEY='votre-cle-secrete'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Migrations et Initialisation
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

## 🧪 Tests

Pour lancer la suite de tests complète :
```bash
python manage.py test
```

## 📦 Production

Pour préparer le déploiement :
1. Passez `DEBUG=False` dans le `.env`.
2. Configurez les `ALLOWED_HOSTS`.
3. Collectez les fichiers statiques : `python manage.py collectstatic`.
4. Utilisez un serveur WSGI comme **Gunicorn**.

---
*Développé pour CLEAN - Solution de gestion environnementale.*
