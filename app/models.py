from app.database import db

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Party(db.Model):
    __tablename__ = 'parties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    rows = db.Column(db.Integer, default=10)
    cols = db.Column(db.Integer, default=10)
    started = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class GameBoard(db.Model):
    __tablename__ = 'game_boards'
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    row = db.Column(db.Integer)
    col = db.Column(db.Integer)
    content = db.Column(db.String(1))  # 0-3

class PlayerParty(db.Model):
    __tablename__ = 'player_parties'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    role = db.Column(db.String(20))
    joined_at = db.Column(db.DateTime, server_default=db.func.now())