from flask import Flask
from routes.auth import auth_routes
from routes.dashboard import dashboard_routes
from routes.main import main_routes
from routes.admin import admin_routes
from db import mysql

app = Flask(__name__)

# 🔐 Chargement de la configuration depuis config.py
app.config.from_object('config')

# 🍪 Configuration des sessions
app.secret_key = app.config.get('SECRET_KEY', 'super-secret-key')  # fallback
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_NAME'] = 'learnball_session'

# 🔗 Initialisation de la base de données
mysql.init_app(app)

# 🔁 Enregistrement des routes via Blueprints
app.register_blueprint(auth_routes)
app.register_blueprint(dashboard_routes)
app.register_blueprint(main_routes)
app.register_blueprint(admin_routes)

# 🚀 Lancement de l'application
if __name__ == '__main__':
    app.run(debug=True)
