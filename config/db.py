from pydantic import BaseSettings


class DBSettings(BaseSettings):

    user: str
    password: str
    db: str
    host: str
    port: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self) -> str:
        """Get database URL."""
        return (
            f"mysql+pymysql://{self.user}:"
            f"{self.password}@{self.host}:{self.port}/{self.db}"
        )


def get_db_settings() -> DBSettings:

    return DBSettings()
