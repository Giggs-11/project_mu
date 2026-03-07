from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: str = "django-insecure-default"
    debug: bool = True
    allowed_hosts: list[str] = ["*"]

    database_name: str = "my_project_db"
    database_user: str = "user"
    database_password: str = "user_password"
    database_host: str = "localhost"
    database_port: int = 3306


settings = Settings()