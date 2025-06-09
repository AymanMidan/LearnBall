from flask import Flask
from routes.auth import auth_routes
from routes.dashboard import dashboard_routes
from routes.main import main_routes
from routes.admin import admin_routes
from routes.api import api_routes
from routes.quiz_routes import quiz_routes
from routes.scientist_api import scientist_routes
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
app.register_blueprint(api_routes)
app.register_blueprint(quiz_routes)
app.register_blueprint(scientist_routes)

# 🚀 Lancement de l'application
if __name__ == '__main__':
    app.run(debug=True)