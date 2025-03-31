#wolf-tcp-server/tcpserver.py
import socket
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import threading

# Connexion à la base de données
conn = psycopg2.connect(
    dbname="wolf_game",
    user="wolf_admin",
    password="motdepasse_secure",
    host="db",
    port="5432"
)
cursor = conn.cursor(cursor_factory=RealDictCursor)

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        request = json.loads(data)
        response = {}

        if request['action'] == 'list_parties':
            cursor.execute("SELECT id_party, title_party FROM parties WHERE is_started = FALSE AND is_finished = FALSE")
            parties = cursor.fetchall()
            response = {
                "id_parties": [party['id_party'] for party in parties],
                "parties_info": {str(party['id_party']): {"title_party": party['title_party']} for party in parties}
            }

        elif request['action'] == 'party_details':
            party_id = request['party_id']
            cursor.execute("""
                SELECT p.id_party, p.title_party, p.grid_size, p.max_players, p.max_turns, p.turn_duration,
                       COUNT(CASE WHEN r.role_name = 'villager' THEN 1 END) as villagers_count,
                       COUNT(CASE WHEN r.role_name = 'werewolf' THEN 1 END) as werewolves_count,
                       COUNT(pip.id_player) as current_players
                FROM parties p
                LEFT JOIN players_in_parties pip ON p.id_party = pip.id_party
                LEFT JOIN roles r ON pip.id_role = r.id_role
                WHERE p.id_party = %s
                GROUP BY p.id_party
            """, (party_id,))
            party = cursor.fetchone()
            response = dict(party) if party else {"error": "Partie non trouvée"}

        elif request['action'] == 'subscribe':
            player = request['player']
            id_party = request['id_party']
            role_preference = request.get("role_preference", "villageois")

            cursor.execute("SELECT id_player FROM players WHERE pseudo = %s", (player,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("INSERT INTO players (pseudo) VALUES (%s) RETURNING id_player", (player,))
                id_player = cursor.fetchone()['id_player']
            else:
                id_player = result['id_player']

            role_name = 'villager' if role_preference == 'villageois' else 'werewolf'
            cursor.execute("SELECT id_role FROM roles WHERE role_name = %s", (role_name,))
            id_role = cursor.fetchone()['id_role']

            cursor.execute("INSERT INTO players_in_parties (id_party, id_player, id_role) VALUES (%s, %s, %s)",
                          (id_party, id_player, id_role))
            conn.commit()

            response = {
                "status": "OK",
                "response": {
                    "role": role_preference,
                    "id_player": id_player
                }
            }

        conn.sendall(json.dumps(response).encode('utf-8'))

    conn.close()


def start_server(host='0.0.0.0', port=8888):  # Port corrigé à 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()
