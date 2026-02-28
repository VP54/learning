from typing import Callable
from polymarket_dashboard.src.config.enum import Exchange
from polymarket_dashboard.src.transform.news.binance import process_binance_announcments
from polymarket_dashboard.src.transform.news.bybit import process_bybit_announcments


RouterType = Callable[[list], list[dict]]

ROUTER_MAPPING: dict[Exchange, RouterType] = {
    Exchange.Binance: process_binance_announcments,
    Exchange.Bybit: process_bybit_announcments,
}

def process_news_announcements(
    announcments: list,
    exchange: Exchange
) -> list[dict]:
    """Process news announcements.
    
    Args:
    ----
        announcements (list): announcements news.
        exchange (Exchange): Exchange enum to route message.

    Returns:
    -------
        list[dict] - list of parsed responses
    """
    try:
        processor = ROUTER_MAPPING[exchange]
    except KeyError:
        raise ValueError(f"No processor registered for {exchange}")

    return processor(announcments)


if __name__ == "__main__":
    import json

    with open("./sample_data/response_binance.json", "r") as f:
        response_binance = json.load(f)

    with open("./sample_data/response_bybit.json", "r") as f:
        response_bybit = json.load(f)

    print(
        process_news_announcements(response_binance, Exchange.Binance)
    )

    print(
        process_news_announcements(response_bybit, Exchange.Bybit)
    )
