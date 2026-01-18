from datetime import datetime
from polymarket_dashboard.src.config.types import Query
from polymarket_dashboard.src.config.enum import QuestDBPartitionBy


def build_drop_table_query(table_name: str) -> Query:
    """"""

    return f"DROP TABLE IF EXISTS {table_name}"

def build_create_table_query(
    table_name: str,
    schema: str,
    partition_by: QuestDBPartitionBy,
    timestamp_col: str="timestamp"
) -> Query:
    """"""
    schema = schema.replace("(", "").replace(")", "")  # in case it is passed as tuple
    query = f"""
        CREATE TABLE IF NOT EXISTS '{table_name}' (
            {schema}
        ) timestamp ({timestamp_col}) PARTITION BY {partition_by} WAL
    """
    return query