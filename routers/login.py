
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.web.async_client import AsyncWebClient

from controller.state import StateController

from login.slack import (
    SlackAuthenticationResponse,
    verify_slack_code
)

from model.state import State
from settings import SETTINGS


authorization_url_generator = AuthorizeUrlGenerator(
    client_id=SETTINGS.slack_client_id,
    redirect_uri=SETTINGS.slack_oauth_redirect_url,
    scopes=[],
    user_scopes=["identity.basic"],
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
    print(f"OAuth callback received - code: {code}, state: {state}")

    if code is not None:
        print(f"Code is valid, attempting to consume state: {state}")
        if state_store.consume(state):
            print("State consumed successfully, requesting token")
            try:
                token_response = await client.openid_connect_token(
                    client_id=SETTINGS.slack_client_id,
                    client_secret=SETTINGS.slack_client_secret,
                    code=code
                )
                print(f"Token response received: {token_response}")

                access_token = token_response.get("access_token")
                id_token = token_response.get("id_token")
                state = token_response.get("state")  # type: ignore
                print(
                    f"Extracted tokens - access_token: {access_token[:20] if access_token else None}..., id_token: {id_token[:20] if id_token else None}...")

                user_info_response = await AsyncWebClient(token=access_token).openid_connect_userInfo()
                print(f"User info response: {user_info_response}")

                protected_data = {"access_token": access_token,
                                  "id_token": id_token, "state": state}
                consent_usr = user_info_response.get("sub")
                print(f"Consent user: {consent_usr}")

                res = {
                    "protected_data": protected_data,
                    "consent_user": consent_usr,
                    "metadata": {**user_info_response.data},  # type: ignore
                }
                print(f"Final response prepared: {res}")
                response = JSONResponse(content=res)
                response.headers["Authorization"] = f"Bearer {access_token}"
                return response

            except Exception as e:
                print(f"Exception occurred during token exchange: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
        else:
            print("Failed to consume state - authorization code has expired")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Authorization code has expired")

    else:
        print("Invalid authorization code received")
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
