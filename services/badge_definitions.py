# badge_definitions.py
# Définitions des badges et conditions d'attribution

# Liste des badges disponibles
BADGES = [
    {
        "id": "perfect_score",
        "name": "Score Parfait",
        "icon": "🏆",
        "description": "Obtenir 100% à un quiz",
        "condition": lambda stats: stats["percentage"] == 100
    },
    {
        "id": "speed_demon",
        "name": "Éclair",
        "icon": "⚡",
        "description": "Temps moyen < 5s par question",
        "condition": lambda stats: stats["avg_time"] < 5
    },
    {
        "id": "streak_master",
        "name": "Sans Faute",
        "icon": "🔥",
        "description": "Obtenir un streak de 5+",
        "condition": lambda stats: stats["max_streak"] >= 5
    },
    {
        "id": "math_genius",
        "name": "Génie des Maths",
        "icon": "🧮",
        "description": "100% en mathématiques",
        "condition": lambda stats: "maths" in stats["category_scores"] and
                                   stats["category_scores"]["maths"]["correct"] == stats["category_scores"]["maths"][
                                       "total"] and
                                   stats["category_scores"]["maths"]["total"] > 0
    },
    {
        "id": "geography_expert",
        "name": "Expert Géo",
        "icon": "🌍",
        "description": "100% en géographie",
        "condition": lambda stats: "geo" in stats["category_scores"] and
                                   stats["category_scores"]["geo"]["correct"] == stats["category_scores"]["geo"][
                                       "total"] and
                                   stats["category_scores"]["geo"]["total"] > 0
    },
    {
        "id": "history_buff",
        "name": "Historien",
        "icon": "📜",
        "description": "100% en histoire",
        "condition": lambda stats: "histoire" in stats["category_scores"] and
                                   stats["category_scores"]["histoire"]["correct"] ==
                                   stats["category_scores"]["histoire"]["total"] and
                                   stats["category_scores"]["histoire"]["total"] > 0
    },
    {
        "id": "rules_master",
        "name": "Arbitre",
        "icon": "📏",
        "description": "100% sur les règles",
        "condition": lambda stats: "regles" in stats["category_scores"] and
                                   stats["category_scores"]["regles"]["correct"] == stats["category_scores"]["regles"][
                                       "total"] and
                                   stats["category_scores"]["regles"]["total"] > 0
    },
    {
        "id": "language_pro",
        "name": "Polyglotte",
        "icon": "🗣️",
        "description": "100% en langues",
        "condition": lambda stats: "langues" in stats["category_scores"] and
                                   stats["category_scores"]["langues"]["correct"] ==
                                   stats["category_scores"]["langues"]["total"] and
                                   stats["category_scores"]["langues"]["total"] > 0
    }
]


def award_badges(stats):
    """
    Évalue les statistiques du quiz et retourne les IDs des badges gagnés

    Args:
        stats (dict): Statistiques du quiz (score, temps, etc.)

    Returns:
        list: Liste des IDs des badges gagnés
    """
    earned_badges = []

    for badge in BADGES:
        try:
            if badge["condition"](stats):
                earned_badges.append(badge["id"])
        except Exception as e:
            # En cas d'erreur dans l'évaluation de la condition (clé manquante, etc.)
            print(f"Erreur lors de l'évaluation du badge {badge['id']}: {e}")
            continue

    return earned_badges

