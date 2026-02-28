from aiohttp import ClientSession
import asyncio


async def make_request(timestamp: int) -> dict[str, any]:
    """Make request with timestamp param.

    Args:
        timestamp (int): timestamp param. Ex.: 1768907700

    Returns:
        ResponseJson
    """
    async with ClientSession() as session:
        url = f"https://gamma-api.polymarket.com/events?slug=btc-updown-15m-{timestamp}"
        async with session.get(url) as response:
            response_json = await response.json()
            return {
                "response": response_json,
                "timestamp": timestamp,
            }


async def fetch_events_using_timestamp(timestamps: list[int]) -> list[dict[str, any]]:
    """Run multiple requests to Polymarket events.

    Args:
        timestamps (list[int]): timestamp param. Ex.: [1768907700, ...]

    Returns:
        list[ResponseJson] - list of responses
    """
    tasks = [
        asyncio.create_task(make_request(timestamp))
        for timestamp in timestamps
    ]
    return await asyncio.gather(*tasks)
