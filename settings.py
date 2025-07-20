
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Define your settings here
    app_name: str = "MLOps Community Platform Score"
    version: str = "1.0.0"

    # NEON database settings
    pg_user: str = "read_only"
    pg_password: str
    pg_database: str = "neondb"
    pg_host: str = "ep-shiny-shadow-adqt5nle-pooler.c-2.us-east-1.aws.neon.tech"
    pg_port: int = 5432

    # Slack oauth settings
    slack_oauth_bot_token: str
    slack_oauth_user_token: str

    # Slack tokens
    slack_app_id: str
    slack_client_id: str
    slack_client_secret: str
    slack_signing_secret: str
    slack_verification_token: str

    # Slack ids
    slack_team_id: str = "T7FHA770F"
    slack_team_name: str


SETTINGS = Settings()  # type: ignore
