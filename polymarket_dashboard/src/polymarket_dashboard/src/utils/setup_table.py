from polymarket_dashboard.src.db.execute_query import build_drop_table_query, build_create_table_query
from polymarket_dashboard.src.db.run_query_http import execute_https_query
from polymarket_dashboard.src.config.logger import logger


__all__ = ["create_table_if_not_exists"]

def create_table_if_not_exists(
    table_name: str,
    schema: str,
    partition_by: str,
    index_columns: str,
    host = "localhost",
    port = "9000",
):
    # drop_query = build_drop_table_query(table_name=table_name)
    # response_drop_table = execute_https_query(host=host, port=port, query=drop_query)
    # logger.info(response_drop_table)

    create_query = build_create_table_query(table_name=table_name, schema=schema, partition_by=partition_by, index_columns=index_columns)
    response_create_table = execute_https_query(host=host, port=port, query=create_query)
    logger.info(response_create_table)
