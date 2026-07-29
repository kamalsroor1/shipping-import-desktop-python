import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Import Management System"
    APP_VERSION: str = "1.0.0"
    
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME: str = os.getenv("DB_NAME", "import_system_db")
    
    # SQLite Fallback for Local Development & Testing if PostgreSQL is not active
    USE_SQLITE_FALLBACK: bool = os.getenv("USE_SQLITE_FALLBACK", "True").lower() in ("true", "1", "t")
    
    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE_FALLBACK:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "import_system.db")
            return f"sqlite:///{db_path}"
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
