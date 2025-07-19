
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/scores", tags=["scoring", "scores", "score"])


@router.get("/")
async def get_scores():
    return {"scores": []}


@router.get("/{platform_id}")
async def get_score(platform_id: str):
    return {"platform_id": platform_id, "score": 42}


@router.post("/{platform_id}")
async def create_score(platform_id: str, score: int):
    return {"platform_id": platform_id, "score": score}
