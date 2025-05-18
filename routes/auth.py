from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from services.auth_service import creer_user, trouver_user_par_identifiant
from werkzeug.security import check_password_hash

auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form['username']
        mot_de_passe = request.form['password']

        user = trouver_user_par_identifiant(identifiant)
        if user and check_password_hash(user.password, mot_de_passe):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['role'] = user.role

            # ✅ Redirection personnalisée selon le rôle
            if user.role == 'admin':
                return redirect('/admin')
            else:
                return redirect('/')
        else:
            flash('❌ Identifiants incorrects. Veuillez réessayer.', 'error')
            return redirect('/login')

    return render_template('login.html')



@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mot_de_passe = request.form['password']

        creer_user(username, email, mot_de_passe)

        # Récupérer le user après inscription
        user = trouver_user_par_identifiant(username)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['role'] = user.role
            return redirect('/')
        else:
            flash("Erreur lors de la création du compte", "error")
            return render_template('signup.html')

    return render_template('signup.html')


@auth_routes.route('/logout')
def logout():
    session.clear()
    # flash("Déconnexion réussie", "success")
    return redirect(url_for('auth.login'))
