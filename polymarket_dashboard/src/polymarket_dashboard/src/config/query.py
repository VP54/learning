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

INDEX_TRADES = """
    exchange
"""

PARTITION_BY = """
    DAY 
"""