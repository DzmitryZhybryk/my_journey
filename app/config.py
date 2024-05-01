import typing

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_serializer
from pathlib import Path


class Settings(BaseSettings):
    RUN_MODE: str = "dev"
    TELEGRAM_BOT_API_TOKEN: SecretStr
    ADMIN_TELEGRAM_ID: SecretStr
    STATIC_STORAGE: Path = Path(__file__).parent.parent.resolve() / 'static'

    # database
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DATABASE: str

    # geocoding
    DISTANCE_SERVICE_URL: str
    DISTANCE_API_KEY: SecretStr
    GEOCODING_SERVICE_URL: str
    GEOCODING_API_KEY: SecretStr

    @field_serializer("TELEGRAM_BOT_API_TOKEN",
                      "ADMIN_TELEGRAM_ID",
                      "GEOCODING_API_KEY",
                      "DISTANCE_API_KEY",
                      when_used='always')
    def dump_secret(self, v: typing.Any) -> typing.Any:
        return v.get_secret_value()

    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')


settings: Settings = Settings()  # type: ignore
