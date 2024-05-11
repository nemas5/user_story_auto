from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):

    user: str
    password: str
    db: str
    host: str
    port: str

    @property
    def db_url(self) -> str:
        """Get database URL."""
        return (
            f"mysql+pymysql://{self.user}:"
            f"{self.password}@{self.host}:{self.port}/{self.db}"
        )

    class Config:
        env_prefix = "MYSQL_"
        env_file = ".env"
        extra = "ignore"


def get_db_settings() -> DBSettings:

    return DBSettings()
