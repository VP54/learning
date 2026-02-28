from pydantic import BaseModel, Field
import os


class DatabaseConfig(BaseModel):
    host: str = Field(default_factory=lambda: os.getenv("DB_HOST",  "localhost"))
    port: int = Field(default_factory=lambda: int(os.getenv("DB_PORT", 9000)))
    username: str = Field(default_factory=lambda: os.getenv("DB_USERNAME", "admin"))
    password: str = Field(default_factory=lambda: os.getenv("DB_PASSWORD", "quest"))
    auto_flush_rows: int = Field(default_factory=lambda: int(os.getenv("DB_AUTO_FLUSH_ROWS", 100)))
    auto_flush_interval: int = Field(default_factory=lambda: int(os.getenv("DB_AUTO_FLUSH_INTERVAL", 1000)))


    def get_connection_string(self) -> str:
        return (
            f"http::addr={self.host}:{self.port};"
            f"username={self.username};password={self.password};"
            f"auto_flush_rows={self.auto_flush_rows};"
            f"auto_flush_interval={self.auto_flush_interval};"
        )