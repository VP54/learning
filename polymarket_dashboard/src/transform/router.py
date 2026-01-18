import logging
from polymarket_dashboard.src.transform.polymarket import parse_polymarket_message
from polymarket_dashboard.src.transform.binance import parse_binance_message


def route_message(message: tuple[str, dict], logger: logging.Logger) -> None:
    msg_type, payload = message
    msg_type = msg_type.lower()

    match msg_type:
        case "binance":
            parse_binance_message(payload, logger)

        case "polymarket":
            parse_polymarket_message(payload, logger)

        case _:
            raise ValueError(f"Unknown message type: {message}")


