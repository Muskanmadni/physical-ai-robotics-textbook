from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from src.models.user import User as UserModel
from src.models.user_progress import UserProgress
from src.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/profile")
async def get_user_profile(current_user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "preferences": user.preferences
    }

@router.put("/users/preferences")
async def update_user_preferences(
    preferences: dict, 
    current_user_id: str, 
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.preferences = preferences
    db.commit()
    
    return {"message": "Preferences updated successfully"}