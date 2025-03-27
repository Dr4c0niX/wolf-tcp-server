from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config import DATABASE_CONFIG
from app.utils.logger import logger

Base = declarative_base()
engine = create_engine(DATABASE_CONFIG['uri'])
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base.query = db_session.query_property()

def init_db():
    try:
        import app.models
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise