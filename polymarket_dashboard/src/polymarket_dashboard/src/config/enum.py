from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class Exchange(StrEnum):
    Polymarket = "POLYMARKET"
    Binance = "BINANCE"


class DatabaseTableNames(str, Enum):
    Binance = "binance_trades"
    Polymarket = "polymarket_trades"
