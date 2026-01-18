import logging


def parse_binance_message(data: dict, logger: logging.Logger):
    logger.debug(f"Parsing message: {data}")


    payload = {
        "symbol": data['s'],
        "open": float(data['o']),
        "volume": float(data['v']),
        "timestamp_binance": data['C']
    }
    logger.debug(payload)
    return payload
