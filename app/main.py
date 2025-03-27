import socketserver
from app.tcp_handler import TCPRequestHandler
from app.database import init_db
from app.utils.logger import logger
from app.config import TCP_SERVER_CONFIG

def run_server():
    init_db()
    host = TCP_SERVER_CONFIG['host']
    port = TCP_SERVER_CONFIG['port']
    
    with socketserver.TCPServer((host, port), TCPRequestHandler) as server:
        logger.info(f"🐺 TCP Server started on {host}:{port}")
        server.serve_forever()

if __name__ == "__main__":
    run_server()