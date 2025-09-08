import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")
BASE_DIR = str(BASE_DIR)


class Config:
    PATH = BASE_DIR
    JWT_KEY = os.getenv("JWT_KEY", "secret")
    ALGORITHM = "HS256"
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{PATH}/database/ecommerce.db")
    TESTING = False
    DEBUG = False


class TestConfig(Config):
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True
    TESTING = True


class DevConfig(Config):
    # A mofifier pour contenairisation
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/database/ecommerce.db")
    JWT_KEY = os.environ.get("JWT_KEY", "secret")
    DEBUG = False
