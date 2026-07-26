from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    POSTGRES_USER: str = "zemr_admin"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "zim_emr"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"
    VECTOR_DIM: int = 384

    BASE_CURRENCY: str = "USD"

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()