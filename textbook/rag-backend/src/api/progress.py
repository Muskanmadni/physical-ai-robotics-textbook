from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.models.user_progress import UserProgress
from src.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/progress")
async def get_user_progress(current_user_id: str, db: Session = Depends(get_db)) -> List[dict]:
    """
    Get user's progress through the textbook
    """
    progress_records = db.query(UserProgress).filter(UserProgress.userId == current_user_id).all()
    
    return [
        {
            "chapterId": progress.chapterId,
            "completed": progress.completed,
            "progressPercentage": progress.progressPercentage
        } for progress in progress_records
    ]

@router.put("/users/progress/{chapter_id}")
async def update_user_progress(
    chapter_id: str,
    progress_data: dict,
    current_user_id: str,
    db: Session = Depends(get_db)
):
    """
    Update progress for a specific chapter
    """
    # Check if progress record already exists
    existing_progress = db.query(UserProgress).filter(
        UserProgress.userId == current_user_id,
        UserProgress.chapterId == chapter_id
    ).first()
    
    if existing_progress:
        # Update existing progress
        existing_progress.completed = progress_data.get("completed", existing_progress.completed)
        existing_progress.progressPercentage = progress_data.get("progressPercentage", existing_progress.progressPercentage)
    else:
        # Create new progress record
        new_progress = UserProgress(
            userId=current_user_id,
            chapterId=chapter_id,
            completed=progress_data.get("completed", False),
            progressPercentage=progress_data.get("progressPercentage", 0)
        )
        db.add(new_progress)
    
    db.commit()
    return {"message": "Progress updated successfully"}