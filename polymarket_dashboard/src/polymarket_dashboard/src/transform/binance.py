import logging
from polymarket_dashboard.src.utils.message_handler import register
from polymarket_dashboard.src.config.enum import Exchange


@register(Exchange.Binance.value)
def parse_binance_message(data: dict, logger: logging.Logger):
    logger.debug(f"Parsing message: {data}")
    payload = {
        "exchange": Exchange.Binance.value,
        "symbol": data['s'],
        "open": float(data['o']),
        "high": float(data['h']),
        "low": float(data['l']),
        "close": float(data['c']),
        "volume": float(data['v']),
        "timestamp_exchange": data['C'] * 1000
    }
    logger.debug(payload)
    return payload
