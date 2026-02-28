import os
from pydantic import BaseModel


class QuestTableConfig(BaseModel):
    table_name: str
    schema: str
    index_columns: str
    partition_by: str
    deduplication_on: str
    timestamp_col: str | None = "timestamp"
    wal: bool = False

    def validate_table_name(self,):
        if not self.table_name.startswith(os.getenv("STAGE")):
            raise ValueError("Table name must start with 'ohlcv_olap_trades'")
