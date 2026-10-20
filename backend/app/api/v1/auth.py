from fastapi import APIRouter, Depends
from backend.app.core.security import get_current_user
from backend.app.db.models import User
from backend.app.schemas.all_schemas import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Return the authenticated user profile mapped from Clerk."""
    return current_user
