import asyncio
from datetime import datetime
from questdb.ingress import Sender
from polymarket_dashboard.src.config.enum import Exchange
from polymarket_dashboard.src.config.models import OHLCVTransactionModel


async def insert_to_db_once(
    db_config: str,
    table_name: str,
    input_queue: asyncio.Queue,
    exchange: Exchange,
    logger,
) -> None:
    with Sender.from_conf(db_config) as sender:
        while True:
            try:
                message = input_queue.get_nowait()
            except asyncio.QueueEmpty:
                logger.info("Queue empty. Done processing.")
                break

            try:
                for row in message:
                    try:
                        OHLCVTransactionModel.model_validate(row)
                    except Exception as e:
                        logger.error(f"Validation error: {e}")
                        continue

                    sender.row(
                        table_name=table_name,
                        at=datetime.fromtimestamp(row['timestamp'] / 1000),
                        symbols={
                            "ticker": row['ticker'],
                            "exchange": exchange.value
                        },
                        columns={
                            "datetime": row['datetime'],
                            "open": row['open'],
                            "high": row['high'],
                            "low": row['low'],
                            "close": row['close'],
                            "volume": row['volume'],
                        },
                    )

                sender.flush()

            finally:
                input_queue.task_done()

    logger.info("DB worker finished.")