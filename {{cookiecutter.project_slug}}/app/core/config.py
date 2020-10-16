from typing import Optional

from pydantic import AnyHttpUrl, AnyUrl, BaseSettings


class Settings(BaseSettings):
    env: str = "local"
    postgres_dsn: AnyUrl = "cockroachdb://root@localhost:29995/{{cookiecutter.project_slug}}"
    postgres_dsn_test: AnyUrl = "cockroachdb://root@localhost:29995/{{cookiecutter.project_slug}}_{}"
    sentry_dsn: Optional[AnyHttpUrl] = None

    # pagination
    default_limit: int = 10
    max_limit: int = 1000


settings = Settings()
