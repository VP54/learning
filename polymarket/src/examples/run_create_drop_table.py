import os, json, requests
from questdb.ingress import Sender, TimestampNanos
from polymarket.src.config.enum import QuestDBPartitionBy
from polymarket.src.db.queries import build_drop_table_query, build_create_table_query
from polymarket.src.db.run_query_http import execute_https_query


host = "localhost"
port = "9000"
conf = f"http::addr={host}:{port};username=admin;password=quest;"


SCHEMA = """
    timestamp TIMESTAMP,
    timestamp_binance SYMBOL,
    symbol SYMBOL,
    open DOUBLE,
    volume DOUBLE
"""


drop_query = build_drop_table_query(table_name="trade_stream")
response_drop_table = execute_https_query(host=host, port=port, query=drop_query)
create_query = build_create_table_query(table_name="trade_stream", schema=SCHEMA, partition_by=QuestDBPartitionBy.DAY)
response_create_table = execute_https_query(host=host, port=port, query=create_query)
