from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from app.services import RetellService

def get_retell_service() -> RetellService:
    """Dependency to get RetellService instance."""
    return RetellService()

# Reusable dependency for database sessions
SessionDep = Annotated[Session, Depends(get_session)]
RetellServiceDep = Annotated[RetellService, Depends(get_retell_service)]
