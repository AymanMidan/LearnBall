from flask import Blueprint, render_template, redirect, session
from models.quiz import UserScore

dashboard_routes = Blueprint('dashboard', __name__)


@dashboard_routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    # Récupérer les scores de l'utilisateur
    user_scores = UserScore.get_user_scores(session['user_id'])

    # Calculer les statistiques
    quiz_count = len(user_scores)

    # Calculer le score moyen
    if quiz_count > 0:
        total_percentage = sum(score.score / score.total_questions * 100 for score in user_scores)
        avg_score = round(total_percentage / quiz_count)
    else:
        avg_score = 0

    # Préparer les données pour le graphique
    chart_labels = []
    chart_data = []

    # Limiter à 10 derniers quiz pour le graphique
    for i, score in enumerate(user_scores[-10:]):
        chart_labels.append(f"Quiz {i + 1}")
        chart_data.append(round(score.score / score.total_questions * 100))

    return render_template('dashboard.html',
                           quiz_count=quiz_count,
                           avg_score=avg_score,
                           chart_labels=chart_labels,
                           chart_data=chart_data)


@dashboard_routes.route('/maths')
def maths():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('maths.html')


@dashboard_routes.route('/geo')
def geo():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('geo.html')


@dashboard_routes.route('/langues')
def langues():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('langues.html')


@dashboard_routes.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('quiz.html')

