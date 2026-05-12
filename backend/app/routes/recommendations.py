from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RecommendationRequest, RecommendationResponse
from app.services import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("", response_model=RecommendationResponse)
def get_recommendations(
    payload: RecommendationRequest,
    db: Session = Depends(get_db),
):
    result = recommendation_service.get_recommendations(
        db=db,
        query=payload.query,
        city=payload.city,
        consultation_type=payload.consultation_type,
    )
    return result
