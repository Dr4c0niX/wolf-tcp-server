from flask import Flask
from routes import api_bp
from database import db_init

app = Flask(__name__)

# Configuration de la base de données
app.config.from_object('config.Config')
db_init(app)

# Enregistrement des routes
app.register_blueprint(api_bp)

if __name__ == '__main__':
    # Lancement du serveur Flask
    app.run(host='0.0.0.0', port=5000)
