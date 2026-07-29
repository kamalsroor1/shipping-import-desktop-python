from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import settings

# Create Engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True if SQL debug query logging is required
    connect_args={"check_same_thread": False} if settings.USE_SQLITE_FALLBACK else {}
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base
Base = declarative_base()

def get_db_session():
    """Context manager / helper for acquiring a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def init_db():
    """Initializes tables in database."""
    Base.metadata.create_all(bind=engine)
