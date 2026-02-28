from polymarket_dashboard.src.config.types import Query
from polymarket_dashboard.src.config.table_config import QuestTableConfig


def build_drop_table_query(table_name: str) -> Query:
    """Dropt able query.

    Args:
        table_name (str): Table name.

    Returns:
        Query
    """
    return f"DROP TABLE IF EXISTS {table_name}"

def build_create_table_query(
    table_config: QuestTableConfig
) -> Query:
    """Build CREATE TABLE query.
    Args:
    ----
        table_name (str): Table name. (Table name in QuestDB)
        schema (str): column type definition. Ex.: timestamp TIMESTAMP, ticker SYMBOL
        index_columns (str): column used for index.
        partition_by (str): column to partition data on.
        timestamp_col (str): Timestamp column.
        upsert_col (str): Optional column for deduplication.
        wal (bool): Whether to use Write-Ahead Logging (WAL) for the table.

    Returns:
    -------
        Query
    """
    schema = table_config.schema.replace("(", "").replace(")", "")  # in case it is passed as tuple
    query = f"""
        CREATE TABLE IF NOT EXISTS '{table_config.table_name}' (
            {schema}
        ), INDEX ({table_config.index_columns}) timestamp ({table_config.timestamp_col}) 
        PARTITION BY {table_config.partition_by} {'WAL' if table_config.wal else ''} 
        {table_config.deduplication_on if table_config.deduplication_on else ''};
    """
    return query