import os
from pydantic import BaseModel, ConfigDict


class OHLCVTransactionModel(BaseModel):
    model_config = ConfigDict(
        strict=True,
        # frozen=True,
    )

    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    datetime: str
    ticker: str
