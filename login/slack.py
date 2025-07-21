
from typing import Annotated

from fastapi import Header

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
    code: str | None = None


async def verify_slack_code(
        slack_header: Annotated[AuthenticationHeader, Header()]
) -> bool:

    if not slack_header.slack_code:
        return False

    print(slack_header.slack_code)

    response = client.oauth_v2_access(
        client_id=SETTINGS.slack_client_id,
        client_secret=SETTINGS.slack_client_secret,
        code=slack_header.slack_code
    ),

    print(response)

    return True
