from flask import Blueprint, render_template, session, redirect
from db import mysql

admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/')

    cur = mysql.connection.cursor()

    # Récupérer les utilisateurs
    cur.execute("SELECT id, username, email, role FROM users")
    utilisateurs = cur.fetchall()

    # Récupérer les messages
    cur.execute("SELECT nom, email, message, date_envoi FROM messages_contact ORDER BY date_envoi DESC")
    messages = cur.fetchall()

    cur.close()

    return render_template("admin.html", utilisateurs=utilisateurs, messages=messages)
