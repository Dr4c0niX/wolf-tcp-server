import socket
import json
import psycopg2
from threading import Thread

# Connexion à la base de données
conn = psycopg2.connect(
    dbname="wolf_game",
    user="wolf_admin",
    password="motdepasse_secure",
    host="db",
    port="5432"
)
cursor = conn.cursor()

def handle_client(conn, addr):
    try:
        data = conn.recv(4096).decode('utf-8')
        if not data:
            return

        request = json.loads(data)
        action = request.get("action")
        parameters = request.get("parameters", {})

        if action == "list_parties":
            cursor.execute("SELECT id_party, title_party FROM parties WHERE is_started = FALSE AND is_finished = FALSE")
            parties = cursor.fetchall()
            parties_data = {"id_parties": [party[0] for party in parties]}
            response = {
                "status": "OK",
                "response": parties_data
            }

        elif action == "subscribe":
            player = parameters.get("player")
            id_party = parameters.get("id_party")

            cursor.execute("SELECT id_player FROM players WHERE pseudo = %s", (player,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO players (pseudo) VALUES (%s) RETURNING id_player", (player,))
                id_player = cursor.fetchone()[0]
            else:
                id_player = result[0]

            cursor.execute("INSERT INTO players_in_parties (id_party, id_player, id_role) VALUES (%s, %s, (SELECT id_role FROM roles WHERE role_name = 'villager' LIMIT 1))", (id_party, id_player))
            conn.commit()

            response = {
                "status": "OK",
                "response": {
                    "role": "villager",
                    "id_player": id_player
                }
            }

        elif action == "create_solo_game":
            player_name = parameters.get("player_name")
            role_preference = parameters.get("role_preference")

            cursor.execute("SELECT id_player FROM players WHERE pseudo = %s", (player_name,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO players (pseudo) VALUES (%s) RETURNING id_player", (player_name,))
                id_player = cursor.fetchone()[0]
            else:
                id_player = result[0]

            cursor.execute("INSERT INTO parties (title_party, is_started, is_finished) VALUES ('Solo Game', FALSE, FALSE) RETURNING id_party")
            id_party = cursor.fetchone()[0]

            cursor.execute("INSERT INTO players_in_parties (id_party, id_player, id_role) VALUES (%s, %s, (SELECT id_role FROM roles WHERE role_name = %s LIMIT 1))", (id_party, id_player, role_preference))
            conn.commit()

            response = {
                "status": "OK",
                "response": {
                    "id_party": id_party,
                    "id_player": id_player
                }
            }

        else:
            response = {"status": "ERROR", "message": "Action inconnue"}

        conn.sendall(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"Erreur lors du traitement de la requête: {e}")
    finally:
        conn.close()

def run_server(host="localhost", port=8888):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Serveur TCP démarré sur {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connexion établie avec {addr}")
            client_thread = Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == "__main__":
    run_server()
