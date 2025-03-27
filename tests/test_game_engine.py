import unittest
from app.game_engine import GameEngine
from app.models import Party, Player
from app.database import db_session

class TestGameEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.party = Party(name="Test")
        db_session.add(self.party)
        db_session.commit()

    def test_list_parties(self):
        response = self.engine.process_request({
            'action': 'list',
            'parameters': []
        })
        self.assertIn(str(self.party.id), response)

    def tearDown(self):
        db_session.rollback()