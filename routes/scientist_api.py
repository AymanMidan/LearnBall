from flask import Blueprint, jsonify, request
from flask_cors import CORS
from models.scientist import Scientist

# Créer le blueprint pour les routes API des scientifiques
scientist_routes = Blueprint('scientist_api', __name__)

# Activer CORS pour toutes les routes de ce blueprint
CORS(scientist_routes)


@scientist_routes.route('/api/scientists', methods=['GET'])
def get_scientists():
    """
    Récupère tous les scientifiques, éventuellement filtrés par catégorie.
    Paramètres de requête:
    - category: Filtrer par catégorie (optionnel)
    """
    try:
        category = request.args.get('category', None)
        scientists = Scientist.get_all(category)

        return jsonify({
            'success': True,
            'data': scientists,
            'count': len(scientists)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/scientists/search', methods=['GET'])
def search_scientists():
    """
    Recherche des scientifiques par nom ou domaine.
    Paramètres de requête:
    - q: Terme de recherche (requis)
    """
    try:
        query = request.args.get('q', '').strip()

        if not query:
            return jsonify({
                'success': False,
                'error': 'Paramètre de recherche manquant'
            }), 400

        scientists = Scientist.search_scientists(query)

        return jsonify({
            'success': True,
            'data': scientists,
            'count': len(scientists),
            'query': query
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/scientists/<scientist_id>', methods=['GET'])
def get_scientist_details(scientist_id):
    """
    Récupère les détails complets d'un scientifique spécifique.
    """
    try:
        scientist = Scientist.get_by_id(scientist_id)

        if not scientist:
            return jsonify({
                'success': False,
                'error': 'Scientifique non trouvé'
            }), 404

        return jsonify({
            'success': True,
            'data': scientist
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Récupère toutes les catégories disponibles avec le nombre de scientifiques.
    """
    try:
        categories = Scientist.get_categories()

        return jsonify({
            'success': True,
            'data': categories
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/scientists/<scientist_id>/quiz', methods=['GET'])
def get_scientist_quiz(scientist_id):
    """
    Récupère uniquement les questions de quiz pour un scientifique.
    """
    try:
        scientist = Scientist.get_quiz(scientist_id)

        if not scientist:
            return jsonify({
                'success': False,
                'error': 'Scientifique non trouvé'
            }), 404

        return jsonify({
            'success': True,
            'data': scientist
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/scientists/<scientist_id>/exam', methods=['GET'])
def get_scientist_exam(scientist_id):
    """
    Récupère uniquement les informations d'examen pour un scientifique.
    """
    try:
        scientist = Scientist.get_exam(scientist_id)

        if not scientist:
            return jsonify({
                'success': False,
                'error': 'Scientifique non trouvé'
            }), 404

        return jsonify({
            'success': True,
            'data': scientist
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/scientists/<scientist_id>/experiment', methods=['GET'])
def get_scientist_experiment(scientist_id):
    """
    Récupère uniquement les informations d'expérience pour un scientifique.
    """
    try:
        scientist = Scientist.get_experiment(scientist_id)

        if not scientist:
            return jsonify({
                'success': False,
                'error': 'Scientifique non trouvé'
            }), 404

        return jsonify({
            'success': True,
            'data': scientist
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@scientist_routes.route('/api/scientists/init', methods=['POST'])
def initialize_database():
    """
    Initialise la base de données avec des données de test.
    Cette route est utile pour le développement et les tests.
    """
    try:
        result = Scientist.initialize_db()

        if result:
            return jsonify({
                'success': True,
                'message': 'Base de données initialisée avec succès'
            }), 200
        else:
            return jsonify({
                'success': True,
                'message': 'Base de données déjà initialisée'
            }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

