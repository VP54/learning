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


SCHEMA_OHLCV_OLAP_TRADES = """
    timestamp TIMESTAMP,
    datetime VARCHAR,
    exchange SYMBOL,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume DOUBLE,
    ticker SYMBOL
"""
INDEX_OHLCV_OLAP_TRADES = "ticker"
PARTITION_OHLCV_OLAP_BY = "DAY"
DEDUPLICATION_OHLCV_OLAP_TRADES = "DEDUP UPSERT KEYS(timestamp, ticker);"



SCHEMA_NEWS = """
    id VARCHAR,
    announcement VARCHAR,
    start_timestamp TIMESTAMP,
    exchange SYMBOL,
    type_event SYMBOL
"""
INDEX_NEWS = "type_event"
PARTITION_NEWS = "DAY"
DEDUPLICATION_NEWS = "DEDUP UPSERT KEYS(id, start_timestamp);"
