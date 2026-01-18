import logging


def parse_side(orderbook_side: list[dict[str, str]], logger: logging.Logger) -> tuple[list[float], list[float]]:
    """Parse orderbook side.

    Args:
        orderbook_side (list[dict[str, str]]): bids/asks.
        logger (logging.Logger): logger.

    Returns:
        tuple[list[float], list[float]]: bid_prices, bid_sizes
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

    return prices, sizes


def parse_polymarket_message(message: dict, logger: logging.Logger):

    logger.debug(f"Parsing message: {message}")

    data = message[0]
    last_price = data["last_trade_price"]
    timestamp = data["timestamp"]
    bids = data["bids"]
    asks = data["asks"]

    parsed_bids = parse_side(bids, logger)
    parsed_asks = parse_side(asks, logger)

    logger.debug(
        f"Timestamp: {timestamp}, Price: {last_price}, Bids: {parsed_bids}, Asks: {parsed_asks}"
    )

    return {
        "timestamp": timestamp,
        "last_price": last_price,
        "bids": parsed_bids,
        "asks": parsed_asks,
    }

if __name__ == "__main__":
    import os, json, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    from polymarket_dashboard.src.config.logger import create_logger
    logger = create_logger(level=logging.DEBUG, name="test_parse_polymarket_message")
    with open("../../data/polymarket_response.json") as f: data = json.load(f)
    response = parse_polymarket_message(data, logger)

    print(response)
