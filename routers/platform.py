
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from controller.platform import (
    MLOpsPlatformController
)

from model.platform import PlatformInformation
from settings import SETTINGS

router = APIRouter(prefix="/platform", tags=["platform", "platforms"])

controller = MLOpsPlatformController(SETTINGS.pg_connection_string)


@router.get("/", tags=["platforms", "all"], summary="Get all platforms")
async def get_all_platforms() -> List[PlatformInformation]:
    return controller.get_all_platforms()


@router.get("/{platform_name}")
async def get_platform(platform_name: str) -> PlatformInformation:
    platform = controller.get_platform_by_name(platform_name)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform


@router.get("/{search_query}")
async def search_platforms(search_query: str) -> List[PlatformInformation]:
    platforms = controller.search_platforms_by_name(search_query)
    if not platforms:
        raise HTTPException(
            status_code=404, detail="No platforms found matching the search query")
    return platforms


@router.get("/paginate")
async def paginate_platforms(page: int = 1, page_size: int = 10) -> List[PlatformInformation]:
    platforms = controller.paginate_platforms(page, page_size)
    if not platforms:
        raise HTTPException(status_code=404, detail="No platforms found")
    return platforms
