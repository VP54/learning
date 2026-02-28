import asyncio
import datetime
import logging
from polymarket_dashboard.src.polymarket_api.request_events import fetch_events_using_timestamp
from polymarket_dashboard.src.polymarket_api.parse_events import parse_message
from polymarket_dashboard.src.utils.add_next_timestamp_interval import get_next_intervals
from polymarket_dashboard.src.config.logger import create_logger


async def add_asset_ids(current_asset_ids: list[str], now: datetime.datetime = None, logger: logging.Logger = None):
    logger = logger or create_logger(__name__)
    now = now or datetime.datetime.utcnow()
    minute = now.minute
    modulo_residue = minute % 15
    if modulo_residue == 14:
        logger.info("Fetching new markets")
        market_timestamps = get_next_intervals(now=now, logger=logger)
        responses = await fetch_events_using_timestamp(market_timestamps)
        asset_id_timestamp_dict = await parse_message(responses)
        current_asset_ids = set(current_asset_ids + list(asset_id_timestamp_dict.keys()))
        return list(current_asset_ids), asset_id_timestamp_dict
    else:
        logger.info(f"Modulo residue {modulo_residue}. No action needed.")
    return list(current_asset_ids), None


if __name__ == "__main__":
    current_asset_ids = [
        "20558626845568583487079654554140348563016310225198798174652833003496963173075",
        "60266177083100344737207729452514552169187382154547664824889393735423047637924",
        "80429775431567136175213710819694534414392637635507594642425940783358224600802",
        "80162637547281288825716960861269882577728170270540356289623228280503175094606",
        "58962366611457122974037368219178592572619058890223557925763955882652800319757",
        "55053788988506044459184809376690065240193773458733590115780904333582541534941",
    ]
    mock_now = datetime.datetime(2026, 1, 26, 11, 29, 0)
    current_asset_ids, asset_id_timestamp_dict = asyncio.run(add_asset_ids(current_asset_ids, now=mock_now, logger=None))
    print(current_asset_ids)
