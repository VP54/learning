from typing import Callable
from polymarket_dashboard.src.polymarket_dashboard.src.config.enum import Exchange


Query: str = ""

MessageHandler: Callable[[Exchange | str, object], None] = None
