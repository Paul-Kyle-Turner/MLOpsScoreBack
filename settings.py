
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Define your settings here
    app_name: str = "MLOps Community Platform Score"
    version: str = "1.0.0"

    # NEON database settings
    PG_USER: str = "read_only"
    PG_PASSWORD: str = "npg_3FvhUJIxjk4D"
    PG_DATABASE: str = "neondb"
    PG_HOST: str = "ep-shiny-shadow-adqt5nle-pooler.c-2.us-east-1.aws.neon.tech"
    PG_PORT: int = 5432


SETTINGS = Settings()
