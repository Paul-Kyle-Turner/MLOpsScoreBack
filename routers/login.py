
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.web.async_client import AsyncWebClient

from controller.state import StateController

from login.slack import (
    SLACK_COOKIE_NAME,
    SlackAuthenticationResponse,
    verify_slack_code
)

from model.state import State
from settings import SETTINGS


authorization_url_generator = AuthorizeUrlGenerator(
    client_id=SETTINGS.slack_client_id,
    redirect_uri=SETTINGS.slack_oauth_redirect_url,
    scopes=[],
    user_scopes=["identity.basic", 'openid'],
)

state_store = StateController(SETTINGS.pg_connection_string)

client = AsyncWebClient(token=SETTINGS.slack_oauth_bot_token)

router = APIRouter(prefix="/v1/slack", tags=["login"])


@router.get("/oauth")
async def oauth() -> JSONResponse:
    state: State | None = state_store.issue()
    if not state:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create state for OAuth"
        )
    url = authorization_url_generator.generate(state=state.state)
    return JSONResponse(
        {
            "redirect_url": url,
        }
    )


@router.get("/oauth_redirect")
async def oauth_callback(code: str, state: str):

    if code is not None:
        if state_store.consume(state):
            try:
                token_response = await client.openid_connect_token(
                    client_id=SETTINGS.slack_client_id,
                    client_secret=SETTINGS.slack_client_secret,
                    code=code
                )

                access_token = token_response.get("access_token")

                if access_token is None:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Access token is missing in the response"
                    )

                response = RedirectResponse(
                    url=SETTINGS.slack_oauth_redirect_home_url
                )
                response.set_cookie(
                    key=SLACK_COOKIE_NAME,
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite="none",
                    # Remove domain restriction for localhost development
                    # domain=SETTINGS.base_domain
                )
                return response

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Authorization code has expired")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid authorization code")


@router.get("/authenticated")
async def login(
    slack_token: Annotated[str | None, Cookie(alias=SLACK_COOKIE_NAME)] = None
) -> JSONResponse:

    if not slack_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token found in cookies"
        )

    # Verify the token with Slack
    try:
        # Use the access token to get user info
        user_client = AsyncWebClient(token=slack_token)
        user_info = await user_client.openid_connect_userInfo()

        if not user_info.get("ok"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        return JSONResponse(content={
            "ok": True,
            "user_info": user_info.data,
            "authenticated": True
        })

    except Exception as e:
        print(f"Error verifying token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to verify authentication token"
        )


@router.get("/user")
async def get_user(
    slack: Annotated[SlackAuthenticationResponse |
                     None, Depends(verify_slack_code)]
) -> JSONResponse:
    """Alternative endpoint using dependency injection for authentication"""

    if slack is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Slack authentication failed, not a valid user or team."
        )

    return JSONResponse(
        content={
            "ok": True,
            "team": slack.team,
            "user": slack.user,
            "team_id": slack.team_id,
            "user_id": slack.user_id,
        }
    )
