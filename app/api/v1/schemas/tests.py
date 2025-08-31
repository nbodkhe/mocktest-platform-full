from pydantic import BaseModel, Field
from typing import Dict

class TestCreate(BaseModel):
    name: str
    duration_minutes: int
    mark_correct: int = 1
    mark_incorrect: int = 0
    subjects: Dict[str, int] = Field(default_factory=dict)

class TestOut(BaseModel):
    id: int
    name: str
    duration_minutes: int
    mark_correct: int
    mark_incorrect: int
    subjects: Dict[str, int]
    status: str
