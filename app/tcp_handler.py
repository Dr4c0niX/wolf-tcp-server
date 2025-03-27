import json
import socketserver
from app.game_engine import GameEngine
from app.utils.json_parser import parse_request
import uuid
import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger instance
logger = logging.getLogger('wolf-game')

def log_request(request_id, message):
    """Log a request with its ID"""
    logger.info(f"[{request_id}] {message}")

class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request_id = str(uuid.uuid4())[:8]
        client_ip = self.client_address[0]
        
        try:
            data = self.request.recv(4096).decode('utf-8').strip()
            if not data:
                return
                
            log_request(request_id, f"📨 Received from {client_ip}: {data[:100]}...")
            
            request = parse_request(data)
            if not request:
                raise ValueError("Invalid JSON format")
            
            response = GameEngine().process_request(request)
            self.request.sendall(response.encode())
            
            log_request(request_id, f"📤 Sent response: {response[:100]}...")
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            logger.error(error_msg)
            self.request.sendall(
                json.dumps({"status": "KO", "error": error_msg}).encode()
            )