from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value


class Exchange(StrEnum):
    Polymarket = "POLYMARKET"
    Binance = "BINANCE"
    Bybit = "BYBIT"


class DatabaseTableNames(str, Enum):
    Binance = "binance_trades"
    Polymarket = "polymarket_trades"


class Timeframe(str, Enum):
    # Seconds
    S1 = "1s"
    S5 = "5s"
    S15 = "15s"
    S30 = "30s"

    # Minutes
    M1 = "1m"
    M3 = "3m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"

    # Hours
    H1 = "1h"
    H2 = "2h"
    H4 = "4h"
    H6 = "6h"
    H12 = "12h"

    # Days
    D1 = "1d"
    D3 = "3d"
    D7 = "1w"


    def to_seconds(self) -> int:
        unit = self.value[-1]
        num = int(self.value[:-1])
        if unit == "s":
            return num
        elif unit == "m":
            return num * 60
        elif unit == "h":
            return num * 3600
        elif unit == "d":
            return num * 86400
        elif unit == "w":
            return num * 604800
        else:
            raise ValueError(f"Unknown timeframe: {self.value}")

class BinanceNewsCategory:
    LISTING = 48
    DELISTING = 161

class NewsCategory:
    LISTING = "listing"
    DELISTING = "delisting"

class ExchangeTimestampUnit(Enum):
    SECONDS = 1
    MILLISECONDS = 1_000
    MICROSECONDS = 1_000_000
    NANOSECONDS = 1_000_000_000

    @property
    def divisor(self) -> int:
        return self.value
