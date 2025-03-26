from flask import Flask, request, jsonify

# Serveur HTTP pour les interactions administratives
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    """Renvoie des données de test."""
    return jsonify({"message": "Hello, World!"})

@app.route('/api/add', methods=['POST'])
def add_data():
    """Ajoute des données via une requête POST."""
    data = request.get_json()
    return jsonify({"message": "Data added successfully!"})

if __name__ == '__main__':
    app.run(port=5001)
