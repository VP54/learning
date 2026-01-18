import logging
from polymarket_dashboard.src.polymarket_dashboard.src.utils.message_handler import get_handler


def route_message(message: tuple[str, str], logger: logging.Logger) -> dict[str, any]:
    """Route message to correct parser.

    Args:
        message (tuple[str, str]): message from websocket queue.
        logger (logging.Logger): logger

    Returns:
        dict[str, any]: parsed message
    """
    msg_type, payload = message
    handler = get_handler(msg_type)
    parsed_message = handler(payload, logger)
    return parsed_message


if __name__ == '__main__':
    import logging
    from polymarket_dashboard.src.polymarket_dashboard.src.config.logger import create_logger
    from polymarket_dashboard.data.polymarket_ws_response import SAMPLE_RESPONSE
    from polymarket_dashboard.data.binance_ws_response import SAMPLE_BINANCE_RESPONSE
    from polymarket_dashboard.src.polymarket_dashboard.src.utils.message_handler import init_handlers
    from polymarket_dashboard.src.polymarket_dashboard.src.config.paths import MESSAGE_HANDLER_PATH

    init_handlers(MESSAGE_HANDLER_PATH)
    logger = create_logger(level=logging.DEBUG, name="test_parse_polymarket_message")
    response = route_message(SAMPLE_RESPONSE, logger)
    print(response)
    response = route_message(SAMPLE_BINANCE_RESPONSE, logger)
    print(response)
