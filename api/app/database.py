from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

settings = get_settings()

# PostgreSQL engine for Supabase
engine = create_engine(
    settings.database_url,
    echo=True,  # Log SQL queries (disable in production)
    pool_pre_ping=True,  # Verify connections before use
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
