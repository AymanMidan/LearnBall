# quiz_routes.py

from flask import Blueprint, jsonify, request, session
from models.quiz import Quiz, UserScore
from db import get_mongo_db
from services.badge_definitions import award_badges, BADGES  # Importer la logique des badges
import random

quiz_routes = Blueprint('quiz_routes', __name__)


@quiz_routes.route('/api/quiz/questions', methods=['GET'])
def get_quiz_questions():
    if 'user_id' not in session:
        return jsonify({'error': 'Non authentifié'}), 401

    limit = int(request.args.get('limit', 10))
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')

    db = get_mongo_db()
    query = {}

    if category and category != 'all':
        query['category'] = category
    if difficulty and difficulty != 'mixte':
        query['difficulty'] = difficulty

    questions = list(db.quiz_questions.find(query))

    if len(questions) > limit:
        questions = random.sample(questions, limit)

    # Retirer l'ID MongoDB pour la sérialisation JSON et s'assurer que 'answer' est un index entier
    processed_questions = []
    for q in questions:
        q.pop('_id', None)
        # Assurer que 'answer' est bien un entier si ce n'est pas déjà le cas
        if 'answer' in q and isinstance(q['answer'], str):
            try:
                q['answer'] = int(q['answer'])
            except ValueError:
                # Gérer le cas où la conversion échoue (donnée invalide)
                # On pourrait logger une erreur ou exclure la question
                continue
        processed_questions.append(q)

    return jsonify(processed_questions)


@quiz_routes.route('/api/quiz/scores', methods=['POST'])
def save_quiz_score():
    if 'user_id' not in session:
        return jsonify({'error': 'Non authentifié'}), 401

    data = request.json

    # Extraire les statistiques détaillées envoyées par le frontend
    stats = {
        "score": data.get('score'),
        "total_questions": data.get('total_questions'),
        "percentage": data.get('percentage'),
        "avg_time": data.get('avg_time'),
        "max_streak": data.get('max_streak'),
        "category_scores": data.get('category_scores', {}),  # Attendu: {'maths': {'correct': 2, 'total': 3}, ...}
        # Ajouter d'autres stats si nécessaire pour les badges futurs
    }

    # Vérifier que les données nécessaires sont présentes
    required_keys = ["score", "total_questions", "percentage", "avg_time", "max_streak", "category_scores"]
    if not all(key in data for key in required_keys):
        return jsonify({'error': 'Données statistiques manquantes ou invalides'}), 400

    # Calculer les badges gagnés côté serveur
    earned_badge_ids = award_badges(stats)

    # Créer l'objet UserScore avec les badges calculés côté serveur
    score_entry = UserScore(
        user_id=session['user_id'],
        score=stats['score'],
        total_questions=stats['total_questions'],
        category=data.get('category', 'mixte'),  # Catégorie générale du quiz joué
        difficulty=data.get('difficulty', 'mixte'),  # Difficulté générale
        time_taken=stats['avg_time'],  # Utiliser le temps moyen ici
        streak=stats['max_streak'],  # Utiliser le streak max
        badges_earned=earned_badge_ids  # Utiliser les badges calculés
    )

    # Sauvegarder le score en base de données
    try:
        UserScore.save_score(score_entry)
    except Exception as e:
        # Log l'erreur
        print(f"Erreur lors de la sauvegarde du score: {e}")
        return jsonify({'error': 'Erreur interne lors de la sauvegarde du score'}), 500

    # Préparer les détails des badges gagnés pour la réponse (sans la fonction condition qui n'est pas sérialisable)
    earned_badges_details = []
    for badge in BADGES:
        if badge["id"] in earned_badge_ids:
            # Créer une copie du badge sans la fonction condition
            badge_copy = {k: v for k, v in badge.items() if k != 'condition'}
            earned_badges_details.append(badge_copy)

    # Retourner un message de succès avec les badges gagnés
    return jsonify({
        'message': 'Score enregistré avec succès',
        'earned_badges': earned_badges_details  # Renvoyer les détails des badges gagnés (sans les fonctions)
    })


@quiz_routes.route('/api/quiz/scores/user', methods=['GET'])
def get_user_quiz_scores():
    if 'user_id' not in session:
        return jsonify({'error': 'Non authentifié'}), 401

    try:
        scores = UserScore.get_user_scores(session['user_id'])
        return jsonify([score.to_dict() for score in scores])
    except Exception as e:
        # Log l'erreur
        print(f"Erreur lors de la récupération des scores utilisateur: {e}")
        return jsonify({'error': 'Erreur interne lors de la récupération des scores'}), 500


# Potentiellement ajouter une route pour récupérer les définitions des badges
@quiz_routes.route('/api/badges/definitions', methods=['GET'])
def get_badge_definitions():
    # Exclure la fonction 'condition' qui n'est pas sérialisable en JSON
    serializable_badges = [
        {k: v for k, v in badge.items() if k != 'condition'}
        for badge in BADGES
    ]
    return jsonify(serializable_badges)


