#!/bin/bash

# ==============================================================================
# Script de déploiement optimisé pour CLEAN PRO sur PythonAnywhere
# Usage: ./deploy_pa.sh <votre_nom_utilisateur_pa>
# ==============================================================================

if [ -z "$1" ]; then
    echo "❌ Erreur: Usage: ./deploy_pa.sh <votre_nom_utilisateur_pa>"
    exit 1
fi

USER_PA=$1
PROJECT_DIR="/home/$USER_PA/clean-visionit"
VENV_NAME="clean-env"
PYTHON_VERSION="3.10"
WSGI_FILE="/var/www/${USER_PA//./_}_pythonanywhere_com_wsgi.py"

echo "--- 🚀 Début du déploiement pour $USER_PA ---"

# 1. Mise à jour du code
if [ -d "$PROJECT_DIR" ]; then
    echo "--- 📥 Mise à jour du code via Git ---"
    cd $PROJECT_DIR
    git pull origin main
else
    echo "--- 📥 Clonage du dépôt ---"
    cd /home/$USER_PA
    git clone https://github.com/nickosamba/clean-visionit.git
    cd $PROJECT_DIR
fi

# 2. Vérification du fichier .env
if [ ! -f ".env" ]; then
    echo "⚠️  AVERTISSEMENT: Le fichier .env est manquant dans $PROJECT_DIR"
    echo "   Assurez-vous de le créer avec vos clés secrètes avant de lancer l'app."
fi

# 3. Gestion de l'environnement virtuel
if [ ! -d "/home/$USER_PA/.virtualenvs/$VENV_NAME" ]; then
    echo "--- 📦 Création de l'environnement virtuel ---"
    mkvirtualenv --python=/usr/bin/python$PYTHON_VERSION $VENV_NAME
else
    echo "--- 📦 Activation de l'environnement virtuel ---"
    # Utilisation de source pour assurer l'activation dans le shell courant
    source /home/$USER_PA/.virtualenvs/$VENV_NAME/bin/activate
fi

# 4. Sauvegarde de sécurité de la base de données (si SQLite)
if [ -f "db.sqlite3" ]; then
    echo "--- 💾 Sauvegarde de la base de données ---"
    cp db.sqlite3 "db.sqlite3.bak.$(date +%Y%m%d_%H%M%S)"
fi

# 5. Installation des dépendances
echo "--- 🛠️ Installation/Mise à jour des dépendances ---"
pip install --upgrade pip
pip install -r requirements.txt

# 6. Migrations
echo "--- 🗄️ Exécution des migrations ---"
python manage.py migrate --noinput

# 7. Fichiers Statiques
echo "--- 🎨 Collecte des fichiers statiques ---"
python manage.py collectstatic --noinput

# 8. Nettoyage des fichiers temporaires/tests
echo "--- 🧹 Nettoyage ---"
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
rm -f paiements/testes/reproduce_bugs.py # Supprimer le script de debug

# 9. Rechargement de l'application Web
echo "--- ♻️ Rechargement de l'application Web ---"
if [ -f "$WSGI_FILE" ]; then
    touch $WSGI_FILE
    echo "✅ Application rechargée."
else
    echo "⚠️  Fichier WSGI non trouvé ($WSGI_FILE). "
    echo "   Si c'est votre premier déploiement, configurez-le dans l'onglet Web de PythonAnywhere."
fi

echo "--- ✨ Déploiement terminé avec succès ! ---"
