from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    otel_collector_endpoint: str = "localhost:4317"
