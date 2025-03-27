import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from app.config import LOGGING_CONFIG
import os

class RequestFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(self, 'request_id', 'SYSTEM')
        return True

request_filter = RequestFilter()

def setup_logging():
    Path(LOGGING_CONFIG['dir']).mkdir(exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(request_id)-8s | %(message)s'
    )
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    file = TimedRotatingFileHandler(
        filename=os.path.join(LOGGING_CONFIG['dir'], 'wolf_tcp.log'),
        when='midnight',
        backupCount=7
    )
    file.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(LOGGING_CONFIG['level'])
    logger.addHandler(console)
    logger.addHandler(file)
    logger.addFilter(request_filter)
    
    return logger

logger = setup_logging()

def log_request(request_id, message):
    request_filter.request_id = request_id
    logger.info(message)