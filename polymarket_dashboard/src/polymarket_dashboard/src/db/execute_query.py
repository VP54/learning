from polymarket_dashboard.src.polymarket_dashboard.src.config.types import Query


def build_drop_table_query(table_name: str) -> Query:
    """"""

    return f"DROP TABLE IF EXISTS {table_name}"

def build_create_table_query(
    table_name: str,
    schema: str,
    index_columns: str,
    partition_by: str,
    timestamp_col: str="timestamp"
) -> Query:
    """"""
    schema = schema.replace("(", "").replace(")", "")  # in case it is passed as tuple
    query = f"""
        CREATE TABLE IF NOT EXISTS '{table_name}' (
            {schema}
        ), INDEX ({index_columns}) timestamp ({timestamp_col}) PARTITION BY {partition_by}
    """
    return query