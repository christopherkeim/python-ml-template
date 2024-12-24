from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    host: str
    port: str
    log_level: str

    model_config = SettingsConfigDict(env_file=".env")


CONFIGS: Configs = Configs()
