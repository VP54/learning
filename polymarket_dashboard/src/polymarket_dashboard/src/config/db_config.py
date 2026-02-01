from pydantic import BaseModel, Field
import os


class DatabaseConfig(BaseModel):
    database: str
    host: str = Field(default_factory=lambda: os.getenv("DB_HOST"))
    port: int = Field(default_factory=lambda: int(os.getenv("DB_PORT")))
    username: str = Field(default_factory=lambda: os.getenv("DB_USERNAME"))
    password: str = Field(default_factory=lambda: os.getenv("DB_PASSWORD"))
