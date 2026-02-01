import os
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    database: str
    host: str = os.getenv("DB_HOST")
    port: int = os.getenv("DB_PORT")
    username: str = os.getenv("DB_USERNAME")
    password: str = os.getenv("DB_PASSWORD")
