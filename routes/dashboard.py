from flask import Blueprint, render_template, redirect, session

dashboard_routes = Blueprint('dashboard', __name__)

@dashboard_routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

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

