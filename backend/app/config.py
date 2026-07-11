import os
from pathlib import Path

from dotenv import load_dotenv


# Project root: E:\ai-database-copilot
BASE_DIR = Path(__file__).resolve().parents[2]

# Project root-এর .env file load করবে
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)


class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME: str = "AI Database Copilot"
    APP_VERSION: str = "0.2.0"

    APP_DATABASE_URL: str = os.getenv("APP_DATABASE_URL", "")
    READER_DATABASE_URL: str = os.getenv("READER_DATABASE_URL", "")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    FERNET_KEY: str = os.getenv("FERNET_KEY", "")

    def validate(self) -> None:
        """Required environment variables পরীক্ষা করবে."""

        missing_variables: list[str] = []

        if not self.APP_DATABASE_URL:
            missing_variables.append("APP_DATABASE_URL")

        if not self.READER_DATABASE_URL:
            missing_variables.append("READER_DATABASE_URL")

        if not self.JWT_SECRET_KEY:
            missing_variables.append("JWT_SECRET_KEY")

        if not self.FERNET_KEY:
            missing_variables.append("FERNET_KEY")

        if missing_variables:
            missing_text = ", ".join(missing_variables)

            raise RuntimeError(
                f"Missing environment variables: {missing_text}. "
                "Please check the project root .env file."
            )


settings = Settings()
settings.validate()