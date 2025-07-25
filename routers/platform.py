
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from controller.platform import (
    MLOpsPlatformController
)

from login.slack import SlackAuthenticationResponse, verify_slack_code
from model.paginate import PaginateRequest
from model.platform import PlatformInformation
from model.search import SearchRequest
from settings import SETTINGS

router = APIRouter(prefix="/platform", tags=["platform", "platforms"])

controller = MLOpsPlatformController(SETTINGS.pg_connection_string)


@router.get("/", tags=["platforms", "all"], summary="Get all platforms")
async def get_all_platforms() -> List[PlatformInformation]:
    return controller.get_all_platforms()


@router.post("/create", tags=["platforms", "create"], summary="Create a new platform")
async def create_platform(
    platform: PlatformInformation,
    slack: Annotated[SlackAuthenticationResponse | None, Depends(
        verify_slack_code
    )]
) -> PlatformInformation:
    if slack is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Slack authentication failed, not a valid user or team."
        )

    return await controller.create_platform(platform)


@router.get("/exists/{platform_name}", tags=["platforms", "exists"], summary="Check if platform exists")
async def platform_exists(platform_name: str) -> List[PlatformInformation]:
    exists = await controller.search_platforms_with_pinecone(platform_name)
    if exists:
        return exists
    return []


@router.get("/{platform_name}", tags=["platforms", "single"], summary="Get platform by name")
async def get_platform_by_name(platform_name: str) -> PlatformInformation:
    platform = controller.get_platform_by_name(platform_name)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform


@router.get("/id/{platform_id}", tags=["platforms", "single"], summary="Get platform by ID")
async def get_platform_by_id(platform_id: int) -> PlatformInformation:
    platform = controller.get_platform(platform_id)
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform


@router.post("/paginate", tags=["platforms", "paginate", "all"], summary="Paginate platforms")
async def paginate_platforms(paginate: PaginateRequest) -> List[PlatformInformation]:
    # TODO add filtering options
    platforms = controller.paginate_platforms(
        page=paginate.page,
        page_size=paginate.page_size
    )
    if not platforms:
        raise HTTPException(status_code=404, detail="No platforms found")
    return platforms


@router.post("/search", tags=["platforms", "search"], summary="Search platforms by name")
async def search_platforms(search_query: SearchRequest) -> List[PlatformInformation]:
    platforms = await controller.search_platforms_with_pinecone(search_query.search_query)

    if not platforms:
        return []
    return platforms
