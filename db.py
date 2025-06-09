from flask_pymysql import MySQL
from pymongo import MongoClient
from flask import current_app

# Singleton pour MySQL (Flask gère déjà l'instance comme Singleton)
mysql = MySQL()

# Singleton manuel pour MongoDB
class MongoSingleton:
    _client = None
    _db = None

    @classmethod
    def get_db(cls):
        if cls._client is None:
            cls._client = MongoClient(current_app.config['MONGO_URI'])
            cls._db = cls._client[current_app.config['MONGO_DB']]
        return cls._db

# Fonction utilitaire
def get_mongo_db():
    return MongoSingleton.get_db()
