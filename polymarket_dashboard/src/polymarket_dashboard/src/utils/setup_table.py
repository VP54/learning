from polymarket_dashboard.src.polymarket_dashboard.src.config.query import SCHEMA_TRADES, INDEX_TRADES, PARTITION_BY
from polymarket_dashboard.src.polymarket_dashboard.src.db.queries import build_drop_table_query, build_create_table_query
from polymarket_dashboard.src.polymarket_dashboard.src.db.run_query_http import execute_https_query
from polymarket_dashboard.src.polymarket_dashboard.src.config.logger import logger


__all__ = ["create_table_if_not_exists"]

def create_table_if_not_exists(
    host = "localhost",
    port = "9000",
    TABLE_NAME = "polymarket_binance_trade_stream",
):
    drop_query = build_drop_table_query(table_name=TABLE_NAME)
    response_drop_table = execute_https_query(host=host, port=port, query=drop_query)
    logger.info(response_drop_table)

    create_query = build_create_table_query(table_name=TABLE_NAME, schema=SCHEMA_TRADES, partition_by=PARTITION_BY, index_columns=INDEX_TRADES)
    response_create_table = execute_https_query(host=host, port=port, query=create_query)
    logger.info(response_create_table)
