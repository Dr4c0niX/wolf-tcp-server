from flask import Blueprint, request, jsonify
from models import db, Player, Game

api_bp = Blueprint('api', __name__)

@api_bp.route('/players', methods=['POST'])
def add_player():
    data = request.get_json()
    new_player = Player(username=data['username'], role=data['role'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Player added'}), 201

@api_bp.route('/games', methods=['POST'])
def create_game():
    data = request.get_json()
    new_game = Game(name=data['name'], max_players=data['max_players'])
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game created'}), 201