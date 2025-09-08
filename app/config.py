# import os


class Config:
    PATH = "E:/Blent/1 - API/my-ecommerce-api"
    JWT_KEY = "secret"
    ALGORITHM = "HS256"
    DATABASE_URL = f"sqlite:///{PATH}/database/ecommerce.db"
