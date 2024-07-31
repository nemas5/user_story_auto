from pydantic import BaseSettings
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))


class DBSettings(BaseSettings):

    user: str
    password: str
    db: str
    host: str
    port: str

    class Config:
        env_prefix = "M_"
        env_file = ".env"

    @property
    def db_url(self) -> str:
        """Get database URL."""
        return (
            f"mysql+pymysql://{self.user}:"
            f"{self.password}@{self.host}:{self.port}/{self.db}"
        )


def get_db_settings() -> DBSettings:
    """Return an instance APISettings."""
    return DBSettings()
