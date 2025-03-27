from models import Party, Player
from database import Database

class GameEngine:
    def __init__(self):
        self.db = Database()
        self.current_party_id = 0  # Pour générer des ID uniques

    def list_open_parties(self):
        return [pid for pid, p in self.db.parties.items() if not p.started]

    def subscribe_player(self, player_name, party_id):
        # Créer une partie si elle n'existe pas
        if party_id not in self.db.parties:
            self.db.parties[party_id] = Party(
                id=party_id,
                players=[],
                started=False,
                board="000000000"
            )
        
        party = self.db.parties[party_id]
        role = "wolf" if len(party.players) % 2 == 0 else "villager"
        player_id = len(party.players) + 1
        player = Player(id=player_id, name=player_name, role=role)
        party.players.append(player)
        
        return {"role": role, "id_player": player_id}