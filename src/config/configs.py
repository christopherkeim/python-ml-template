from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    HOST: str
    PORT: str
    LOG_LEVEL: str
    LOG_FORMAT: Literal["standard", "json"] = "json"

    model_config = SettingsConfigDict(env_file=".env")


CONFIGS: Configs = Configs()
