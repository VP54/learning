from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

class QuestDBPartitionBy(StrEnum):
    DAY = "DAY"
    MONTH = "MONTH"
    YEAR = "YEAR"
