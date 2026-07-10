import os
from pathlib import Path

from dotenv import load_dotenv


# Project root:
# E:\ai-database-copilot
BASE_DIR = Path(__file__).resolve().parents[2]

# Project root-এর .env file load করবে
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)


class Settings:
    """Application configuration loaded from environment variables."""

    APP_NAME: str = "AI Database Copilot"
    APP_VERSION: str = "0.1.0"

    APP_DATABASE_URL: str | None = os.getenv("APP_DATABASE_URL")
    READER_DATABASE_URL: str | None = os.getenv("READER_DATABASE_URL")

    def validate(self) -> None:
        """Required environment variables আছে কি না পরীক্ষা করবে."""

        missing_variables = []

        if not self.APP_DATABASE_URL:
            missing_variables.append("APP_DATABASE_URL")

        if not self.READER_DATABASE_URL:
            missing_variables.append("READER_DATABASE_URL")

        if missing_variables:
            missing_text = ", ".join(missing_variables)

            raise RuntimeError(
                f"Missing environment variables: {missing_text}. "
                "Please check the project root .env file."
            )


settings = Settings()
settings.validate()