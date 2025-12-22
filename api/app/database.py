from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

settings = get_settings()

# SQLite engine (use check_same_thread=False for FastAPI)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=True,  # Log SQL queries (disable in production)
)


def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
