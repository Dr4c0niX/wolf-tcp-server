from flask import Flask
from routes import api_bp
from database import db_init

app = Flask(__name__)

app.config.from_object('config.Config')
db_init(app)

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
