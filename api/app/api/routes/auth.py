from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse, RefreshRequest
from app.services.auth import AuthService
from app.api.deps import AuthServiceDep, CurrentUserDep

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, auth_service: AuthServiceDep):
    """Authenticate user and return tokens."""
    try:
        result = await auth_service.sign_in(request.email, request.password)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, auth_service: AuthServiceDep):
    """Refresh access token."""
    try:
        result = await auth_service.refresh_session(request.refresh_token)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"]
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: CurrentUserDep):
    """Get authenticated user info."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email
    )