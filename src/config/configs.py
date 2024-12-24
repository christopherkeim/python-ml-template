from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    host: str
    port: str
    log_level: str
    log_format: Literal["standard", "json"]

    model_config = SettingsConfigDict(env_file=".env")


CONFIGS: Configs = Configs()
