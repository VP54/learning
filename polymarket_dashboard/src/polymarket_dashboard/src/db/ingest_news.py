from datetime import datetime
from questdb.ingress import Sender
from polymarket_dashboard.src.config.enum import Exchange, ExchangeTimestampUnit


EXCHANGE_TIMESTAMP_UNIT = {
    Exchange.Bybit: ExchangeTimestampUnit.SECONDS,
    Exchange.Binance: ExchangeTimestampUnit.MILLISECONDS,
}

def insert_news_to_db(
    db_config: str,
    table_name: str,
    rows: list[dict],
    exchange: Exchange,
    logger,
) -> None:
    """Ingest news about ICO to QuestDB.
    
    Args:
    ----
        db_config (str): DB config string
        table_name (str): table name in QuestDB
        rows (list[dict]): rows to insert as a list of rows as dict
        exchange (Exchange): Exchange enum with value
        logger,

    Returns:
    -------
        None
    """

    with Sender.from_conf(db_config) as sender:

        for row in rows:

            sender.row(
                table_name=table_name,

                # Must match TIMESTAMP(start_timestamp)
                at=datetime.fromtimestamp(
                    row["releaseDate"] / EXCHANGE_TIMESTAMP_UNIT[exchange].divisor
                ),

                # SYMBOL columns
                symbols={
                    "exchange": exchange.value,
                    "type_event": row["type_event"],
                },

                # Regular columns
                columns={
                    "id": str(row["id"]),
                    "announcement": row["title"],
                },
            )

        sender.flush()

    logger.info(f"Inserted {len(rows)} news rows.")
