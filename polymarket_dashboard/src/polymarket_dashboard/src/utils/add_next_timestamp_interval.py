import logging
import datetime


def get_next_intervals(now: datetime.datetime, logger: logging.Logger) -> list[int]:
    """Get next fifteen minute interval.

    Args:
        now (datetime.datetime): The current time.
        logger (logging.Logger): The logger.

    Returns:
        list[int]: The next 4 fifteen minute interval.
    """
    market_timestamps = []
    minute = now.minute
    next_moment = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute + 1, 0)
    for i in range(4):
        market_timestamps.append(
            int(
                (
                    next_moment + i * datetime.timedelta(minutes=15)
                ).timestamp()
            )
        )

    logger.info(f"Fetched {len(market_timestamps)} markets.")
    return market_timestamps