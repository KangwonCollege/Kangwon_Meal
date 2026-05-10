from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_host: str | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None
    db_port: int = 3306
    db_path: str = "./kangwon_meal.db"

    # Cloud SQL (Unix socket) — Cloud Run 배포 시 사용
    # 형식: PROJECT_ID:REGION:INSTANCE_NAME
    cloud_sql_instance: str | None = None

    @property
    def use_sqlite(self) -> bool:
        return not all([self.db_user, self.db_password, self.db_name])

    @property
    def use_cloud_sql(self) -> bool:
        return self.cloud_sql_instance is not None and not self.use_sqlite


@lru_cache
def get_settings() -> Settings:
    return Settings()
