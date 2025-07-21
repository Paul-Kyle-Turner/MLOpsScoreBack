
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.web.async_client import AsyncWebClient

from login.slack import (
    SlackAuthenticationResponse,
    verify_slack_code
)

from settings import SETTINGS


authorization_url_generator = AuthorizeUrlGenerator(
    client_id=SETTINGS.slack_client_id,
    redirect_uri=SETTINGS.slack_oauth_redirect_url,
    scopes=[],
    user_scopes=["identity.basic"],
)
state_store = FileOAuthStateStore(expiration_seconds=300)

client = AsyncWebClient(token=SETTINGS.slack_oauth_bot_token)

router = APIRouter(prefix="/v1/slack", tags=["login"])


@router.get("/oauth")
async def oauth() -> JSONResponse:
    state = state_store.issue()
    url = authorization_url_generator.generate(state=state)
    print(f"Generated OAuth URL: {url}")
    return JSONResponse(
        {
            "redirect_url": url,
        }
    )


@router.get("/slack/oauth_redirect")
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
                id_token = token_response.get("id_token")
                state = token_response.get("state")  # type: ignore

                user_info_response = await AsyncWebClient(token=access_token).openid_connect_userInfo()
                protected_data = {"access_token": access_token,
                                  "id_token": id_token, "state": state}
                consent_usr = user_info_response.get("sub")

                res = {
                    "protected_data": protected_data,
                    "consent_user": consent_usr,
                    "metadata": {**user_info_response.data},  # type: ignore
                }
                response = JSONResponse(content=res)
                response.headers["Authorization"] = f"Bearer {access_token}"
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


@router.get("/login")
async def login(
    slack: Annotated[SlackAuthenticationResponse | None, Depends(
        verify_slack_code
    )],
) -> JSONResponse:
    if slack is None or slack.code is None:
        raise HTTPException(
            status_code=403,
            detail="Slack authentication failed, not a valid user or team."
        )

    response = JSONResponse(
        content={
            "ok": True,
            "team": slack.team,
            "user": slack.user,
        }
    )

    response.set_cookie(
        key="X-Slack-Code",
        value=slack.code
    )

    return response
