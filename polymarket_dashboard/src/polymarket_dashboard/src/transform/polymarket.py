import logging
import numpy as np
from polymarket_dashboard.src.utils.message_handler import register
from polymarket_dashboard.src.config.enum import Exchange


def parse_side(orderbook_side: list[dict[str, str]], logger: logging.Logger) -> np.array:
    """Parse orderbook side.

    Args:
        orderbook_side (list[dict[str, str]]): bids/asks.
        logger (logging.Logger): logger.

    Returns:
        np.array: bid_prices, bid_sizes
    """
    float_ = float
    prices, sizes = [], []

    append_price = prices.append
    append_size = sizes.append

    for side in orderbook_side:
        append_price(float_(side['price']))
        append_size(float_(side['size']))

    logger.debug(f"Polymarket Orderbook Prices: {prices}")
    logger.debug(f"Polymarket Orderbook Sizes: {sizes}")

    return np.array([prices, sizes], np.float64)


@register(Exchange.Polymarket.value)
def parse_polymarket_message(message: dict, logger: logging.Logger):

    logger.debug(f"Parsing message: {message}")

    data = message
    last_price = data.get("last_trade_price", None)
    timestamp = int(data["timestamp"])
    bids = data["bids"]
    asks = data["asks"]

    parsed_bids = parse_side(bids, logger)
    parsed_asks = parse_side(asks, logger)

    logger.debug(
        f"Timestamp: {timestamp}, Price: {last_price}, Bids: {parsed_bids}, Asks: {parsed_asks}"
    )

    return {
        "timestamp_exchange": timestamp,
        "last_price": last_price,
        "bids": parsed_bids,
        "asks": parsed_asks,
        "exchange": Exchange.Polymarket.value,
    }

if __name__ == "__main__":
    import os, json, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    from polymarket_dashboard.src.polymarket_dashboard.src.config.logger import create_logger
    logger = create_logger(level=logging.DEBUG, name="test_parse_polymarket_message")
    with open("../../../../data/polymarket_response.json") as f: data = json.load(f)
    response = parse_polymarket_message(data, logger)

    print(response)
