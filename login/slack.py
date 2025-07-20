
from typing import Annotated

from fastapi import Header

from pydantic import BaseModel

from slack_sdk import WebClient

from settings import SETTINGS

client = WebClient(token=SETTINGS.slack_oauth_bot_token)


class SlackAuthenticationResponse(BaseModel):
    ok: bool
    url: str | None = None
    team: str | None = None
    user: str | None = None
    team_id: str | None = None
    user_id: str | None = None


async def slack_code(
        slack_code: Annotated[str | None, Header()]
) -> bool:

    response = SlackAuthenticationResponse.model_validate(
        client.auth_test(token=slack_code)
    )

    if SETTINGS.slack_team_id and SETTINGS.slack_team_id != response.team_id:
        return False

    if SETTINGS.slack_team_name and SETTINGS.slack_team_name != response.team:
        return False

    return True
