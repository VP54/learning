import ast
from polymarket_dashboard.src.config.types import EventID

Timestamp: int = 0


async def parse_message(responses: list[dict[str, any]]) -> dict[EventID, Timestamp]:
    """Extract event id from responses.

    Args:
        responses (list[ResponseJson]): The responses received from the server.

    Returns:
        tuple[EventID, Timestamp]: The event ids extracted from the responses. (Asset ID)
    """
    dct = {}
    for response in responses:
        _response = response["response"]
        event_timestamp = response["timestamp"]
        club_token_ids = ast.literal_eval(_response[0]["markets"][0]['clobTokenIds'])
        for id in club_token_ids:
            dct[id] = event_timestamp

    return dct


