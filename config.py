import os
from datetime import timedelta

# Configuration de base
SECRET_KEY = os.urandom(24).hex()  # Clé aléatoire à chaque démarrage
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'learnball'

# Configuration des sessions
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # 30 minutes max