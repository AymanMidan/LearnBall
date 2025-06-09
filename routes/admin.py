from flask import Blueprint, render_template, session, redirect, request, jsonify, flash
from db import mysql
import json
from datetime import datetime, timedelta

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

    # Calculer les statistiques
    stats = get_admin_statistics()

    cur.close()

    return render_template("admin.html",
                           utilisateurs=utilisateurs,
                           messages=messages,
                           stats=stats)


def get_admin_statistics():
    """Récupère les statistiques pour le tableau de bord admin"""
    cur = mysql.connection.cursor()

    # Nombre d'utilisateurs
    cur.execute("SELECT COUNT(*) FROM users")
    nb_utilisateurs = cur.fetchone()[0]

    # Nombre de messages
    cur.execute("SELECT COUNT(*) FROM messages_contact")
    nb_messages = cur.fetchone()[0]

    # Statistiques des visites (simulées pour l'exemple)
    # Dans un vrai projet, vous auriez une table de logs de visites
    nb_visites = 834  # Valeur simulée

    # Activité (pourcentage d'utilisateurs actifs dans les 30 derniers jours)
    # Simulé pour l'exemple
    activite = 76  # Pourcentage simulé

    # Données pour les graphiques
    # Visites des 7 derniers jours (simulées)
    visites_chart = {
        'labels': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        'data': [120, 150, 180, 200, 170, 160, 140]
    }

    # Distribution des rôles
    cur.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    roles_data = cur.fetchall()

    roles_chart = {
        'labels': [role[0] for role in roles_data],
        'data': [role[1] for role in roles_data]
    }

    cur.close()

    return {
        'nb_utilisateurs': nb_utilisateurs,
        'nb_messages': nb_messages,
        'nb_visites': nb_visites,
        'activite': activite,
        'visites_chart': visites_chart,
        'roles_chart': roles_chart
    }


@admin_routes.route('/admin/api/users')
def get_users():
    """API pour récupérer la liste des utilisateurs"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, role FROM users ORDER BY id DESC")
    users = cur.fetchall()
    cur.close()

    users_list = []
    for user in users:
        users_list.append({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3]
        })

    return jsonify(users_list)


@admin_routes.route('/admin/api/messages')
def get_messages():
    """API pour récupérer la liste des messages"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nom, email, sujet, message, date_envoi FROM messages_contact ORDER BY date_envoi DESC")
    messages = cur.fetchall()
    cur.close()

    messages_list = []
    for message in messages:
        messages_list.append({
            'id': message[0],
            'nom': message[1],
            'email': message[2],
            'sujet': message[3],
            'message': message[4],
            'date_envoi': message[5].strftime('%Y-%m-%d %H:%M:%S') if message[5] else 'N/A'
        })

    return jsonify(messages_list)


@admin_routes.route('/admin/api/stats')
def get_stats():
    """API pour récupérer les statistiques"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    stats = get_admin_statistics()
    return jsonify(stats)


@admin_routes.route('/admin/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Supprimer un utilisateur"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True, 'message': 'Utilisateur supprimé avec succès'})


@admin_routes.route('/admin/user/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    """Modifier le rôle d'un utilisateur"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    data = request.get_json()
    new_role = data.get('role')

    if new_role not in ['user', 'admin', 'moderator']:
        return jsonify({'error': 'Rôle invalide'}), 400

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True, 'message': 'Rôle mis à jour avec succès'})


@admin_routes.route('/admin/message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """Supprimer un message"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM messages_contact WHERE id = %s", (message_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True, 'message': 'Message supprimé avec succès'})


@admin_routes.route('/admin/message/<int:message_id>/read', methods=['PUT'])
def mark_message_read(message_id):
    """Marquer un message comme lu"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    # Ajouter une colonne 'lu' à la table messages_contact si elle n'existe pas
    try:
        cur.execute("ALTER TABLE messages_contact ADD COLUMN lu BOOLEAN DEFAULT FALSE")
        mysql.connection.commit()
    except:
        pass  # La colonne existe déjà

    cur.execute("UPDATE messages_contact SET lu = TRUE WHERE id = %s", (message_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'success': True, 'message': 'Message marqué comme lu'})


@admin_routes.route('/admin/users/export')
def export_users():
    """Exporter la liste des utilisateurs en CSV"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, role, created_at FROM users")
    users = cur.fetchall()
    cur.close()

    # Créer le contenu CSV
    csv_content = "ID,Nom d'utilisateur,Email,Rôle,Date de création\n"
    for user in users:
        csv_content += f"{user[0]},{user[1]},{user[2]},{user[3]},{user[4]}\n"

    from flask import Response
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=utilisateurs.csv"}
    )


@admin_routes.route('/admin/messages/export')
def export_messages():
    """Exporter la liste des messages en CSV"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    cur = mysql.connection.cursor()
    cur.execute("SELECT nom, email, sujet, message, date_envoi FROM messages_contact")
    messages = cur.fetchall()
    cur.close()

    # Créer le contenu CSV
    csv_content = "Nom,Email,Sujet,Message,Date d'envoi\n"
    for message in messages:
        # Échapper les guillemets dans le message
        message_text = str(message[3]).replace('"', '""')
        csv_content += f'"{message[0]}","{message[1]}","{message[2]}","{message_text}","{message[4]}"\n'

    from flask import Response
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=messages.csv"}
    )


@admin_routes.route('/admin/search')
def search():
    """Recherche dans les utilisateurs et messages"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Accès non autorisé'}), 403

    query = request.args.get('q', '')
    search_type = request.args.get('type', 'all')  # 'users', 'messages', 'all'

    results = {'users': [], 'messages': []}

    if not query:
        return jsonify(results)

    cur = mysql.connection.cursor()

    if search_type in ['users', 'all']:
        # Recherche dans les utilisateurs
        cur.execute("""
            SELECT id, username, email, role 
            FROM users 
            WHERE username LIKE %s OR email LIKE %s
        """, (f'%{query}%', f'%{query}%'))
        users = cur.fetchall()

        for user in users:
            results['users'].append({
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'role': user[3]
            })

    if search_type in ['messages', 'all']:
        # Recherche dans les messages
        cur.execute("""
            SELECT id, nom, email, sujet, message, date_envoi 
            FROM messages_contact 
            WHERE nom LIKE %s OR email LIKE %s OR sujet LIKE %s OR message LIKE %s
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        messages = cur.fetchall()

        for message in messages:
            results['messages'].append({
                'id': message[0],
                'nom': message[1],
                'email': message[2],
                'sujet': message[3],
                'message': message[4][:100] + '...' if len(message[4]) > 100 else message[4],
                'date_envoi': message[5].strftime('%Y-%m-%d %H:%M:%S') if message[5] else 'N/A'
            })

    cur.close()
    return jsonify(results)

