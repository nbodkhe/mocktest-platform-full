from pydantic import BaseModel
from typing import List

class QuestionCreate(BaseModel):
    test_id: int
    subject: str
    stem: str
    options: List[str]
    correct_index: int
    difficulty: int = 1

class QuestionOut(BaseModel):
    id: int
    test_id: int
    subject: str
    stem: str
    options: list
    correct_index: int
    difficulty: int
