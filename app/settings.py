from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    otel_collector_endpoint: str = "localhost:4317"
    environment: str = "dev"
    running_unittests: int = 0


settings = Settings()
