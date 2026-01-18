import logging


def parse_message(message: str, logger: logging.Logger):
    logger.info(f"Parsing message: {message}")

    data = message[1]

    payload = {
        "symbol": data['s'],
        "open": float(data['o']),
        "volume": float(data['v']),
        "timestamp_binance": data['C']
    }
    logger.info(payload)
    return payload
