from db import mysql
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import Utilisateur

def trouver_user_par_identifiant(identifiant):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s OR email=%s", (identifiant, identifiant))
    user = cur.fetchone()
    cur.close()
    return Utilisateur(*user) if user else None

def creer_user(username, email, password, role="student"):
    hashed = generate_password_hash(password)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed, role))
    mysql.connection.commit()
    cur.close()
