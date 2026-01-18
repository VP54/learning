import logging
from polymarket_dashboard.src.polymarket_dashboard.src.utils.message_handler import register
from polymarket_dashboard.src.polymarket_dashboard.src.config.enum import Exchange


@register(Exchange.Binance)
def parse_binance_message(data: dict, logger: logging.Logger):
    logger.debug(f"Parsing message: {data}")

    payload = {
        "exchange": Exchange.Binance.value,
        "symbol": data['s'],
        "open": float(data['o']),
        "volume": float(data['v']),
        "timestamp_binance": data['C']
    }
    logger.debug(payload)
    return payload
