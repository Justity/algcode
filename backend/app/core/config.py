from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Controller Emulator"
    debug: bool = False
    api_prefix: str = "/api"

    telemetry_interval_seconds: float = 1.0
    min_response_delay_ms: int = 50
    max_response_delay_ms: int = 350
    random_error_probability: float = 0.08

    websocket_path: str = "/ws"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()