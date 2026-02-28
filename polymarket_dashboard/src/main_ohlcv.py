import os
import datetime
import time
from dotenv import load_dotenv
from polymarket_dashboard.src.config.enum import Exchange, Timeframe
from polymarket_dashboard.src.db.execute_query import build_create_table_query
from polymarket_dashboard.src.db.run_query_http import execute_https_query
from polymarket_dashboard.src.config.query import SCHEMA_OHLCV_OLAP_TRADES, INDEX_OHLCV_OLAP_TRADES, PARTITION_OHLCV_OLAP_BY, DEDUPLICATION_OHLCV_OLAP_TRADES
from polymarket_dashboard.src.config.table_config import QuestTableConfig
from polymarket_dashboard.src.config.db_config import DatabaseConfig
from polymarket_dashboard.src.transform.ohlcv.ccxt_ohlcv import ohlcv_parser
from polymarket_dashboard.src.transform.ohlcv.ccxt_ohlcv import CcxtApi
from polymarket_dashboard.src.db.ingest_ohlcv import insert_to_db
from polymarket_dashboard.src.config.logger import logger


def fix_tokens(tokens):
    return [
        f"{token}/USDT"
        for token in tokens
        if not token.endswith("/USDT")
    ]



async def run_ohlcv_pipeline(since: str, tokens: list[str] = None, until: str=None, timeframe: Timeframe = Timeframe.H1):

    load_dotenv('.env')
    
    client = CcxtApi(exchange_name=Exchange.Binance, logger=logger)
    timeframe = Timeframe.H1
    token = fix_tokens(tokens) if tokens is None else tokens
    since = int(datetime.datetime(2025, 1, 1).timestamp())
    limit = 100
    until = until or int(time.time())
    
    table_config = QuestTableConfig(
        table_name=f"{os.getenv('STAGE')}_ohlcv",
        schema=SCHEMA_OHLCV_OLAP_TRADES,
        index_columns=INDEX_OHLCV_OLAP_TRADES,
        partition_by=PARTITION_OHLCV_OLAP_BY, 
        deduplication_on=DEDUPLICATION_OHLCV_OLAP_TRADES,
        wal=True
    )

    db_config = DatabaseConfig(port=9000)
    conf = db_config.get_connection_string()

    query = build_create_table_query(table_config=table_config)
    execute_https_query(host='localhost', port=9000, query=query, logger=logger)
    ohlcv_queue = await client.fetch_ohlcv_list(
            tokens=tokens, timeframe=timeframe, since=since, limit=limit, until=until
        )

    parsed_data_queue = ohlcv_parser(
            client=client,
            ohlcv_queue=ohlcv_queue,
            max_workers=4,
            logger=logger
        )

    await insert_to_db(
            db_config=conf,
            table_name=table_config.table_name,
            input_queue=parsed_data_queue,
            exchange=Exchange.Binance,
            logger=logger
        )
