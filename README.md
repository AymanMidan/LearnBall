# 🏈 LearnBall - Apprendre avec le Football

Une plateforme d'apprentissage interactive qui combine l'éducation avec la passion du football.

## 🚀 Installation et Configuration

### Prérequis
- Python 3.11+
- MySQL 8.0+
- MongoDB 4.4+
- Git

### Installation

1. **Cloner le projet**
```bash
git clone <url-du-projet>
cd learnball
```

2. **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de données MySQL**
```bash
# Se connecter à MySQL
mysql -u root -p

# Créer la base de données
source sql/create_database.sql

# Insérer les données d'exemple
source sql/insert_sample_data.sql
```

4. **Configurer les variables d'environnement**
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=votre_mot_de_passe
export MYSQL_DB=learnball
export MONGO_URI=mongodb://localhost:27017/learnball
export SECRET_KEY=votre-clé-secrète
```

5. **Démarrer l'application**
```bash
python app.py
```

L'application sera accessible sur `http://127.0.0.1:5000`

## 🎯 Fonctionnalités

### 🔐 Authentification
- Inscription et connexion sécurisées
- Gestion des rôles (étudiant, enseignant, administrateur)
- Hachage des mots de passe avec Werkzeug

### 📚 Modules d'Apprentissage
- **📊 Maths**: Statistiques de matchs, probabilités
- **🌍 Géographie**: Clubs et joueurs internationaux
- **🗣️ Langues**: Apprentissage avec interviews de stars
- **🧠 Quiz**: Défis de connaissances footballistiques et académiques

### 🏆 Système de Récompenses
- Badges automatiques basés sur les performances
- Classements et compétitions
- Suivi des progrès personnalisés

### 📊 Tableau de Bord
- Statistiques détaillées par utilisateur
- Historique des quiz et performances
- Graphiques de progression

## 🏗️ Architecture

### Design Patterns Implémentés
- **Singleton**: Gestion des connexions base de données
- **Strategy**: Calcul des badges et récompenses
- **DAO**: Accès aux données abstrait
- **MVC**: Séparation modèle-vue-contrôleur
- **MVVM**: Services comme ViewModels

### Structure du Projet
```
learnball/
├── 📁 models/          # Modèles de données
│   ├── user.py         # Modèle utilisateur
│   ├── quiz.py         # Modèle quiz
│   ├── club.py         # Modèle club
│   └── scientist.py    # Modèle scientifique
├── 📁 services/        # Logique métier
│   ├── auth_service.py # Service d'authentification
│   ├── quiz_service.py # Service de quiz
│   ├── dao.py          # Data Access Objects
│   └── badge_strategies.py # Stratégies de badges
├── 📁 routes/          # Contrôleurs Flask
│   ├── auth.py         # Routes d'authentification
│   ├── quiz_routes.py  # Routes de quiz
│   ├── dashboard.py    # Routes du tableau de bord
│   └── admin.py        # Routes d'administration
├── 📁 templates/       # Templates HTML
├── 📁 static/          # Ressources statiques
├── 📁 uml/            # Diagrammes UML
├── 📁 sql/            # Scripts SQL
├── 📁 docs/           # Documentation
├── app.py             # Point d'entrée
├── config.py          # Configuration
└── db.py              # Gestion BDD
```

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.11**: Langage principal
- **Flask 2.2.5**: Framework web
- **MySQL**: Base de données relationnelle
- **MongoDB**: Base de données NoSQL
- **Flask-PyMySQL**: ORM MySQL
- **PyMongo**: Driver MongoDB

### Frontend
- **HTML5**: Structure sémantique
- **CSS3**: Styles modernes avec animations
- **JavaScript**: Interactivité côté client
- **Design Responsive**: Compatible mobile/desktop

### Sécurité
- **Werkzeug**: Hachage des mots de passe
- **Flask-Session**: Gestion des sessions
- **Validation des données**: Protection contre les injections

## 📋 API Endpoints

### Authentification
- `POST /login` - Connexion utilisateur
- `POST /signup` - Inscription utilisateur
- `GET /logout` - Déconnexion

### Quiz
- `GET /api/quiz/questions` - Récupérer des questions
- `POST /api/quiz/scores` - Sauvegarder un score
- `GET /api/quiz/statistics` - Statistiques utilisateur
- `GET /api/quiz/leaderboard` - Classement

### Administration (Enseignants)
- `POST /admin/quiz/create` - Créer un quiz
- `PUT /admin/quiz/<id>` - Modifier un quiz
- `DELETE /admin/quiz/<id>` - Supprimer un quiz

## 🧪 Tests

### Lancer les tests
```bash
# Tests unitaires
python -m pytest tests/

# Tests d'intégration
python -m pytest tests/integration/

# Tests de bout en bout
python -m pytest tests/e2e/
```

### Couverture de tests
```bash
coverage run -m pytest
coverage report
coverage html
```

## 📊 Monitoring et Logs

### Configuration des logs
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Métriques disponibles
- Nombre d'utilisateurs actifs
- Quiz complétés par jour
- Temps de réponse moyen
- Taux d'erreur

## 🚀 Déploiement

### Environnement de Production

1. **Configuration**
```bash
export FLASK_ENV=production
export DEBUG=False
```

2. **Serveur WSGI**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **Proxy Nginx**
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker (Optionnel)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contribution

### Standards de Code
- Suivre PEP 8 pour Python
- Commentaires en français
- Tests unitaires obligatoires
- Documentation des fonctions

### Workflow Git
1. Fork du projet
2. Créer une branche feature
3. Commits atomiques avec messages clairs
4. Pull request avec description détaillée

## 📄 Licence

Ce projet est développé dans un cadre académique.

## 👥 Équipe

- **Développement**: Équipe LearnBall
- **Architecture**: Design Patterns et Clean Code
- **UI/UX**: Interface moderne et intuitive
- **Tests**: Validation complète

## 📞 Support

Pour toute question ou problème:
- 📧 Email: support@learnball.com
- 📖 Documentation: `/docs/`
- 🐛 Issues: Utiliser le système de tickets

---

**Version**: 1.0.0  
**Dernière mise à jour**: 8 Juin 2025  
**Statut**: ✅ Production Ready

