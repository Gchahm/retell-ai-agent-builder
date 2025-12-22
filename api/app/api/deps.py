from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.database import get_session

# Reusable dependency for database sessions
SessionDep = Annotated[Session, Depends(get_session)]
