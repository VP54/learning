SCHEMA_TRADES = """
    timestamp TIMESTAMP,
    timestamp_exchange TIMESTAMP,
    exchange SYMBOL,
    bids DOUBLE[][],
    asks DOUBLE[][],
    ticker SYMBOL,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume DOUBLE
"""
INDEX_TRADES = "exchange"
PARTITION_BY = "DAY"


SCHEMA_BINANCE_TRADES = """
    timestamp TIMESTAMP,
    timestamp_exchange TIMESTAMP,
    exchange SYMBOL,
    ticker SYMBOL,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume DOUBLE
"""
INDEX_BINANCE_TRADES = "exchange"
PARTITION_BINANCE_BY = "DAY"


SCHEMA_POLYMARKET_TRADES = """
    timestamp TIMESTAMP,
    timestamp_exchange TIMESTAMP,
    exchange SYMBOL,
    bids DOUBLE[][],
    asks DOUBLE[][],
    ticker SYMBOL,
    price DOUBLE,
    asset_id SYMBOL,
    market SYMBOL
"""
INDEX_POLYMARKET_TRADES = "exchange"
PARTITION_POLYMARKET_BY = "DAY"