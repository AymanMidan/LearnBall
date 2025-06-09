from flask import Blueprint, jsonify, request
from models.club import Club

api_routes = Blueprint('api', __name__)

@api_routes.route('/api/clubs', methods=['GET'])
def get_clubs():
    clubs = Club.get_all()
    return jsonify([club.to_dict() for club in clubs])

@api_routes.route('/api/clubs/<name>', methods=['GET'])
def get_club(name):
    club = Club.get_by_name(name)
    if club:
        return jsonify(club.to_dict())
    return jsonify({'error': 'Club non trouvé'}), 404

@api_routes.route('/api/clubs/continent/<continent>', methods=['GET'])
def get_clubs_by_continent(continent):
    clubs = [club for club in Club.get_all() if club.continent.lower() == continent.lower()]
    return jsonify([club.to_dict() for club in clubs])