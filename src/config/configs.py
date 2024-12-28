from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: str = "8000"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["standard", "json"] = "json"

    model_config = SettingsConfigDict(env_file=".env")


CONFIGS: Configs = Configs()
