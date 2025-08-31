from pydantic import BaseModel
from datetime import datetime

class SessionCreate(BaseModel):
    test_id: int
    user_id: int

class SessionOut(BaseModel):
    id: int
    test_id: int
    user_id: int
    start_at: datetime
    end_at: datetime | None
    status: str
