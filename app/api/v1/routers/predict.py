from fastapi import APIRouter
from pydantic import BaseModel
from app.domain.percentiles import predict_percentiles

router = APIRouter(prefix="/predict")

class PredictIn(BaseModel):
    total_score: float
    subject_scores: dict
    real_distribution: dict

@router.post("")
async def predict(payload: PredictIn):
    pct_overall, pct_subjects = predict_percentiles(payload.total_score, payload.subject_scores, payload.real_distribution)
    return {"percentile_overall": pct_overall, "percentile_subjects": pct_subjects}
