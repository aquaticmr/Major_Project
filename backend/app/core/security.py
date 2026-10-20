from typing import Optional, Dict, Any
import httpx
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.db.session import get_db
from backend.app.db.models import User

security_scheme = HTTPBearer(auto_error=False)

# Cached JWKS client
jwks_client: Optional[PyJWKClient] = None
if settings.CLERK_JWKS_URL and "clerk" in settings.CLERK_JWKS_URL:
    try:
        jwks_client = PyJWKClient(settings.CLERK_JWKS_URL, cache_keys=True, max_cached_keys=16)
    except Exception as e:
        logger.warning(f"Failed to initialize Clerk JWKS client: {e}")

async def verify_clerk_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)) -> Dict[str, Any]:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # Check for test/dev bypass if in testing/local environment with mock token
    if settings.APP_ENV in ["development", "testing"] and token.startswith("test_token_"):
        clerk_id = token.replace("test_token_", "")
        return {
            "sub": clerk_id,
            "email": f"{clerk_id}@example.com",
            "name": f"User {clerk_id}",
            "role": "admin" if "admin" in clerk_id else "user"
        }

    try:
        # Retrieve signing key from JWKS
        if not jwks_client:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Clerk JWKS client is not configured"
            )
        
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decode_kwargs = {
            "algorithms": ["RS256"],
            "options": {"verify_aud": bool(settings.CLERK_AUDIENCE)}
        }
        if settings.CLERK_AUDIENCE:
            decode_kwargs["audience"] = settings.CLERK_AUDIENCE
        if settings.CLERK_ISSUER_URL:
            decode_kwargs["issuer"] = settings.CLERK_ISSUER_URL

        payload = jwt.decode(
            token,
            signing_key.key,
            **decode_kwargs
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidIssuerError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"JWT verification failure: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or signature",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_user(
    payload: Dict[str, Any] = Depends(verify_clerk_token),
    db: Session = Depends(get_db)
) -> User:
    clerk_user_id = payload.get("sub")
    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain a valid user identity (sub)"
        )
    
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    if not user:
        # Lazy user synchronization
        email = payload.get("email") or payload.get("email_address")
        name = payload.get("name") or payload.get("first_name", "")
        role = payload.get("role", "user")
        
        user = User(
            clerk_user_id=clerk_user_id,
            email=email,
            display_name=name,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required"
        )
    return current_user
