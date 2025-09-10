import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class Config:
    JWT_KEY = os.getenv("JWT_KEY", "secret")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/database/ecommerce.db")
    TESTING = False
    DEBUG = False


class TestConfig(Config):
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True
    TESTING = True


class DevConfig(Config):
    # A mofifier pour containerisation
    # DATABASE_URL = "sqlite:///:memory:"
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/database/ecommerce.db")
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/database/ecommerce.db")
    JWT_KEY = os.getenv("JWT_KEY", "secret")
    DEBUG = False


CONFIG_MAP = {
    "dev": DevConfig,
    "testing": TestConfig,
    "prod": ProdConfig
}