from app.models import Player, Party, GameBoard, PlayerParty
from app.database import db_session
from sqlalchemy.exc import SQLAlchemyError
import random
from datetime import datetime
from app.utils.json_parser import format_response
from app.utils.logger import logger

class GameEngine:
    def process_request(self, request):
        try:
            action = request.get('action')
            params = {p['name']: p['value'] for p in request.get('parameters', [])}
            
            handlers = {
                'list': self.list_open_parties,
                'subscribe': self.subscribe_to_party,
                'party_status': self.get_party_status,
                'gameboard_status': self.get_gameboard_status,
                'move': self.process_move
            }
            
            if action in handlers:
                return handlers[action](params)
            return format_response("KO", "Invalid action")
            
        except Exception as e:
            logger.error(f"Engine error: {e}")
            return format_response("KO", str(e))

    def list_open_parties(self, params):
        parties = Party.query.filter_by(started=False).all()
        return format_response("OK", {"id_parties": [p.id for p in parties]})

    def subscribe_to_party(self, params):
        player_name = params.get('player')
        party_id = params.get('id_party')
        
        party = Party.query.get(party_id)
        if not party:
            return format_response("KO", "Party not found")
        
        player = Player.query.filter_by(name=player_name).first() or Player(name=player_name)
        db_session.add(player)
        
        role = 'wolf' if random.random() > 0.7 else 'villager'
        db_session.add(PlayerParty(
            player_id=player.id,
            party_id=party_id,
            role=role,
            joined_at=datetime.now()
        ))
        db_session.commit()
        
        return format_response("OK", {"role": role, "id_player": player.id})

    def get_party_status(self, params):
        # Implémentation simplifiée
        return format_response("OK", {
            "party": {
                "id_party": params.get('id_party'),
                "started": False,
                "round_in_progress": -1
            }
        })

    def get_gameboard_status(self, params):
        # Implémentation simplifiée
        return format_response("OK", {"visible_cells": "0"*9})

    def process_move(self, params):
        # Implémentation simplifiée
        return format_response("OK", {
            "round_in_progress": 1,
            "move": {"next_position": {"row": 0, "col": 1}}
        })