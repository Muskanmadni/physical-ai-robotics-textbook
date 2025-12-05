from fastapi import APIRouter, Depends, HTTPException
from src.models.quiz import Quiz
from src.models.quiz_submission import QuizSubmission
from src.utils.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "questions": quiz.questions
    }

@router.post("/quizzes/{quiz_id}/submit")
async def submit_quiz(quiz_id: str, 
                      answers: dict, 
                      current_user_id: str, 
                      db: Session = Depends(get_db)):
    """
    Submit a quiz attempt and calculate score
    """
    # Verify the quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score based on answers
    correct_answers = 0
    total_questions = len(quiz.questions)
    
    for i, question in enumerate(quiz.questions):
        if i < len(answers) and str(answers[i]) == str(question.get('correctAnswer', '')):
            correct_answers += 1
    
    score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
    
    # Save the submission
    quiz_submission = QuizSubmission(
        id=f"submission-{quiz_id}-{current_user_id}",
        quizId=quiz_id,
        userId=current_user_id,
        answers=answers,
        score=score
    )
    
    db.add(quiz_submission)
    db.commit()
    
    return {
        "id": quiz_submission.id,
        "quizId": quiz_id,
        "userId": current_user_id,
        "score": score,
        "completedAt": quiz_submission.completedAt
    }