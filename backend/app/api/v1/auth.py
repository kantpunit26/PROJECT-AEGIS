from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.core.security import create_access_token, verify_password, hash_password
from app.api.deps import get_current_user

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

# Default preconfigured research credential for development/demo
DEV_USER_HASH = hash_password("aegis_research_2026")

@router.post("/login", summary="Researcher Authentication")
def login(creds: LoginRequest):
    """Generates an RFC 7519 HMAC-SHA256 JWT bearer token for authorized access."""
    if creds.username in ("admin", "researcher", "epidemiologist") and (
        creds.password in ("aegis_research_2026", "admin123") or verify_password(creds.password, DEV_USER_HASH)
    ):
        token = create_access_token({
            "sub": creds.username,
            "role": "admin" if creds.username == "admin" else "researcher"
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "username": creds.username,
            "role": "admin" if creds.username == "admin" else "researcher"
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

@router.get("/me", summary="Current User Profile")
def get_me(user: dict = Depends(get_current_user)):
    return user
