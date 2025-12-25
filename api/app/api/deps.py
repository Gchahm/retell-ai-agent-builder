from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.database import get_session
from app.services import RetellService, PostProcessingService
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth import AuthService
from app.supabase import get_supabase_client

security = HTTPBearer()

def get_auth_service() -> AuthService:
    return AuthService(get_supabase_client())

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: AuthServiceDep
):
    """Extract and validate JWT, return user."""
    token = credentials.credentials
    user = await auth_service.get_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

CurrentUserDep = Annotated[any, Depends(get_current_user)]

def get_retell_service() -> RetellService:
    """Dependency to get RetellService instance."""
    return RetellService()


def get_post_processing_service() -> PostProcessingService:
    """Dependency to get RetellService instance."""
    return PostProcessingService()


# Reusable dependency for database sessions
SessionDep = Annotated[Session, Depends(get_session)]
RetellServiceDep = Annotated[RetellService, Depends(get_retell_service)]
PostProcessingServiceDep = Annotated[PostProcessingService, Depends(get_post_processing_service)]
