from pydantic import BaseModel

class SubmissionIn(BaseModel):
    test_id: int
    user_id: int
    question_id: int
    chosen_index: int

class SubmissionOut(BaseModel):
    is_correct: bool
    total_score: float
    subject_scores: dict
