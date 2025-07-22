
from typing import Annotated

from fastapi import Cookie, Header

from pydantic import AliasChoices, BaseModel

from slack_sdk import WebClient

from settings import SETTINGS

client = WebClient(token=SETTINGS.slack_oauth_bot_token)


class AuthenticationHeader(BaseModel):
    slack_code: str | None = Header(
        default=None,
        validation_alias=AliasChoices(
            "X-Slack-Code",
            "x-slack-code",
            "slack_code",
            "slack-code",
        )  # type: ignore
    )


class SlackAuthenticationResponse(BaseModel):
    ok: bool
    url: str | None = None
    team: str | None = None
    user: str | None = None
    team_id: str | None = None
    user_id: str | None = None


SLACK_COOKIE_NAME = "slack_access_token"


async def verify_slack_code(
        slack_access_token: Annotated[str | None, Cookie(
            validation_alias=AliasChoices(
                "slack_access_token",
                "slack-access-token",
                SLACK_COOKIE_NAME
            )  # type: ignore
        )]
) -> SlackAuthenticationResponse | None:

    if not slack_access_token:
        return None

    try:
        # Use the access token to get user info
        from slack_sdk.web.async_client import AsyncWebClient
        user_client = AsyncWebClient(token=slack_access_token)
        user_info = await user_client.openid_connect_userInfo()

        if not user_info.get("ok"):
            return None

        # user_info["data"] contains the user information
        user_data = user_info.get("user", {})

        return SlackAuthenticationResponse(
            ok=True,
            user_id=user_data.get("sub"),
            user=user_data.get("name"),
            team_id=user_data.get("https://slack.com/team_id"),
            team=user_data.get("https://slack.com/team_name"),
        )

    except Exception as e:
        print(f"Error verifying access token: {e}")
        return None
