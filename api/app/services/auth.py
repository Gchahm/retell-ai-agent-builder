from supabase import Client, AuthApiError

class AuthService:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    async def sign_in(self, email: str, password: str) -> dict:
        """Sign in user and return session."""
        response = self.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }

    async def get_user(self, access_token: str):
        """Verify JWT and return user. Returns None if invalid."""
        try:
            response = self.supabase.auth.get_user(access_token)
            return response.user
        except AuthApiError:
            return None

    async def refresh_session(self, refresh_token: str) -> dict:
        """Refresh the session using refresh token."""
        response = self.supabase.auth.refresh_session(refresh_token)
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }