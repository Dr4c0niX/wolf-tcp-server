import socket

# Serveur TCP pour gérer les connexions des joueurs
def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("TCP Server is listening on port 12345")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Welcome to the TCP server!")
        client_socket.close()

if __name__ == "__main__":
    start_tcp_server()
