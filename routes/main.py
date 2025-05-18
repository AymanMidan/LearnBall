from flask import Blueprint, render_template, session, redirect, url_for
from flask import render_template, session
import os
from flask import request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from db import mysql

main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def home():
    return render_template('index.html')

@main_routes.route('/compte')
def compte():
    if 'user_id' not in session:  # Protection de la route
        return redirect(url_for('auth.login'))
    return render_template('compte.html')


# Configuration pour le téléchargement des images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Vérifier si l'extension de fichier est autorisée
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_routes.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Récupérer les données du formulaire
    username = request.form['username']
    email = request.form['email']

    # Mise à jour dans la base de données
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET username=%s, email=%s WHERE id=%s",
                (username, email, session['user_id']))
    mysql.connection.commit()
    cur.close()

    # Mise à jour de la session
    session['username'] = username
    session['email'] = email

    # Redirection avec message de succès
    flash('Profil mis à jour avec succès', 'success')
    return redirect(url_for('main.compte'))


@main_routes.route('/update_photo', methods=['POST'])
def update_photo():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Vérifier si un fichier a été envoyé
    if 'profile_image' not in request.files:
        flash('Aucune image sélectionnée', 'error')
        return redirect(url_for('main.compte'))

    file = request.files['profile_image']

    # Si l'utilisateur n'a pas sélectionné de fichier
    if file.filename == '':
        flash('Aucune image sélectionnée', 'error')
        return redirect(url_for('main.compte'))

    # Si le fichier est valide
    if file and allowed_file(file.filename):
        # Sécuriser le nom du fichier
        filename = secure_filename(f"user_{session['user_id']}_{file.filename}")

        # Créer le dossier d'uploads s'il n'existe pas
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', UPLOAD_FOLDER), exist_ok=True)

        # Enregistrer le fichier
        file_path = os.path.join(os.path.dirname(__file__), '..', UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Mettre à jour la base de données
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET profile_image=%s WHERE id=%s",
                    (filename, session['user_id']))
        mysql.connection.commit()
        cur.close()

        # Mettre à jour la session
        session['profile_image'] = filename

        flash('Photo de profil mise à jour avec succès', 'success')
    else:
        flash('Type de fichier non autorisé. Utilisez JPG, PNG ou GIF', 'error')

    return redirect(url_for('main.compte'))


@main_routes.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Supprimer le compte de la base de données
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (session['user_id'],))
    mysql.connection.commit()
    cur.close()

    # Effacer la session
    session.clear()

    flash('Votre compte a été supprimé avec succès', 'success')
    return redirect(url_for('auth.login'))


@main_routes.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form.get('name')
        email = request.form.get('email')
        sujet = request.form.get('subject')
        message = request.form.get('message')

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO messages_contact (nom, email, sujet, message)
            VALUES (%s, %s, %s, %s)
        """, (nom, email, sujet, message))
        mysql.connection.commit()
        cur.close()

        flash('Votre message a bien été envoyé ✅', 'success')
        return redirect(url_for('main.contact'))

    return render_template("contact.html")
