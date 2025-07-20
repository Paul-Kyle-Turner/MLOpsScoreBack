
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from controller.platform import (
    MLOpsPlatformController
)

from model.paginate import PaginateRequest
from model.platform import PlatformInformation
from settings import SETTINGS

router = APIRouter(prefix="/platform", tags=["platform", "platforms"])

controller = MLOpsPlatformController(SETTINGS.pg_connection_string)


@router.get("/", tags=["platforms", "all"], summary="Get all platforms")
async def get_all_platforms() -> List[PlatformInformation]:
    return controller.get_all_platforms()


@router.get("/{platform_name}", tags=["platforms", "single"], summary="Get platform by name")
async def get_platform(platform_name: str) -> PlatformInformation:
    platform = controller.get_platform_by_name(platform_name)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform


@router.get("/{search_query}", tags=["platforms", "search"], summary="Search platforms by name")
async def search_platforms(search_query: str) -> List[PlatformInformation]:
    platforms = controller.search_platforms_by_name(search_query)
    if not platforms:
        raise HTTPException(
            status_code=404, detail="No platforms found matching the search query")
    return platforms


@router.get("/paginate", tags=["platforms", "paginate", "all"], summary="Paginate platforms")
async def paginate_platforms(paginate: PaginateRequest) -> List[PlatformInformation]:
    # TODO add filtering options
    platforms = controller.paginate_platforms(
        page=paginate.page,
        page_size=paginate.page_size
    )
    if not platforms:
        raise HTTPException(status_code=404, detail="No platforms found")
    return platforms


@router.post("/create", tags=["platforms", "create"], summary="Create a new platform")
async def create_platform(platform: PlatformInformation) -> PlatformInformation:
    return controller.create_platform(platform)
