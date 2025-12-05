from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.models.chapter import Chapter
from src.models.module import Module
from src.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/modules")
async def get_modules(db: Session = Depends(get_db)) -> List[dict]:
    modules = db.query(Module).order_by(Module.order).all()
    return [
        {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "order": module.order
        } for module in modules
    ]

@router.get("/modules/{module_id}/chapters")
async def get_chapters_for_module(module_id: str, db: Session = Depends(get_db)) -> List[dict]:
    chapters = db.query(Chapter).filter(Chapter.module == module_id).order_by(Chapter.order).all()
    if not chapters:
        raise HTTPException(status_code=404, detail="No chapters found for this module")
    
    return [
        {
            "id": chapter.id,
            "title": chapter.title,
            "module": chapter.module,
            "order": chapter.order,
            "language": chapter.language
        } for chapter in chapters
    ]

@router.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: str, 
                     language: str = "en", 
                     user_id: str = None,
                     db: Session = Depends(get_db)):
    # Try to find personalized content if user is specified
    if user_id:
        from src.models.personalized_content import PersonalizedContent
        personalized_content = db.query(PersonalizedContent).filter(
            PersonalizedContent.originalChapterId == chapter_id,
            PersonalizedContent.userId == user_id
        ).first()
        
        if personalized_content:
            return {
                "id": chapter_id,
                "title": personalized_content.title,
                "content": personalized_content.personalizedContent,
                "module": personalized_content.module,
                "order": personalized_content.order,
                "language": language,
                "metadata": personalized_content.metadata
            }
    
    # Otherwise return standard chapter
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    return {
        "id": chapter.id,
        "title": chapter.title,
        "content": chapter.content,
        "module": chapter.module,
        "order": chapter.order,
        "language": chapter.language,
        "metadata": chapter.metadata
    }