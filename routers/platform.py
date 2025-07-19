
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/platform", tags=["platform", "platforms"])


@router.get("/")
async def get_platforms():
    return {"platforms": []}


@router.get("/{platform_id}")
async def get_platform(platform_id: str):
    return {"platform_id": platform_id}


@router.post("/{platform_id}")
async def create_platform(platform_id: str):
    return {"platform_id": platform_id}
