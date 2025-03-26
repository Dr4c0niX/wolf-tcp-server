# Moteur de jeu pour gérer la logique du jeu

class GameEngine:
    def __init__(self):
        self.players = []
        self.roles = ['wolf', 'villager']

    def initialize_game(self):
        """Initialise le jeu avec les joueurs et les rôles."""
        print("Game initialized with players and roles.")

    def move_player(self, player, direction):
        """Déplace un joueur dans une direction donnée."""
        print(f"Player {player} moved {direction}.")

    def assign_roles(self):
        """Assigne des rôles aux joueurs."""
        for player in self.players:
            player['role'] = self.roles[0]  # Exemple simple
