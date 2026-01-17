SCHEMA = """
    timestamp TIMESTAMP,
    timestamp_exchange SYMBOL,
    exchange SYMBOL,
    bids DOUBLE[][],
    asks DOUBLE[][],
    ticker SYMBOL,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume DOUBLE,
    tx_hash HASH,
"""