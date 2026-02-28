import os
import asyncio
from dotenv import load_dotenv
from polymarket_dashboard.src.db.execute_query import build_create_table_query
from polymarket_dashboard.src.db.run_query_http import execute_https_query
from polymarket_dashboard.src.db.ingest_news import insert_news_to_db
from polymarket_dashboard.src.config.query import INDEX_NEWS, SCHEMA_NEWS, PARTITION_NEWS, DEDUPLICATION_NEWS
from polymarket_dashboard.src.config.table_config import QuestTableConfig
from polymarket_dashboard.src.config.db_config import DatabaseConfig
from polymarket_dashboard.src.config.enum import BinanceNewsCategory, Exchange, ExchangeTimestampUnit
from polymarket_dashboard.src.config.logger import logger
from polymarket_dashboard.src.transform.news.router import process_news_announcements
from polymarket_dashboard.src.news.binance import BinanceAnnouncmentScraper
from polymarket_dashboard.src.news.bybit import ByBitAnnouncmentScraper


async def run_binance_pipeline(conf, table_config, num_pages):
    try:
        scraper = BinanceAnnouncmentScraper(logger=logger)
        listing_news = scraper.scrape_announcements(num_pages=10, category_id=BinanceNewsCategory.LISTING)
        delistin_news = scraper.scrape_announcements(num_pages=10, category_id=BinanceNewsCategory.DELISTING)
        parsed_listing_news = process_news_announcements(listing_news, exchange=Exchange.Binance)
        parsed_delisting_news = process_news_announcements(delistin_news, exchange=Exchange.Binance)
        insert_news_to_db(
            db_config=conf, table_name=table_config.table_name, rows=parsed_delisting_news, exchange=Exchange.Binance, logger=logger
        )

        insert_news_to_db(
            db_config=conf, table_name=table_config.table_name, rows=parsed_listing_news, exchange=Exchange.Binance, logger=logger
        )
        return {"ok": True, "msg": ''}
    except Exception as e:
        return {"ok": False, 'msg': e}



async def run_bybit_pipeline(conf, table_config):
    try:
        scraper = ByBitAnnouncmentScraper(logger=logger)
        news = scraper.scrape_announcements(num_pages=20)
        parsed_news = process_news_announcements(news, exchange=Exchange.Binance)
        insert_news_to_db(
            db_config=conf, table_name=table_config.table_name, rows=parsed_news, exchange=Exchange.Bybit, logger=logger
        )
        return {"ok": True, "msg": ''}
    except Exception as e:
        return {"ok": False, 'msg': e}



async def news_etl(pipelines: list[str], num_pages: int):
    """Run news pipelines pipeline.
    
    Args:
    ----
        pipelines
    """
    responses = []
    pipeline = ['binance', 'bybit']
    load_dotenv('.env')
    table_config = QuestTableConfig(
        table_name=f"{os.getenv('STAGE', 'dev')}_news",
        schema=SCHEMA_NEWS,
        index_columns=INDEX_NEWS,
        partition_by=PARTITION_NEWS, 
        deduplication_on=DEDUPLICATION_NEWS,
        timestamp_col="start_timestamp",
        wal=True
    )
    db_config = DatabaseConfig(port=9000)
    conf = db_config.get_connection_string()
    query = build_create_table_query(table_config=table_config)
    execute_https_query(host='localhost', port=9000, query=query, logger=logger)

    for pipeline in pipelines:
        match pipeline.lower():
            case "binance":
                response_binance = await run_binance_pipeline(conf=conf, table_config=table_config)
                responses.append(response_binance)
            case "bybit":
                response_bybit = await run_bybit_pipeline(conf=conf, table_config=table_config)
                responses.append(response_bybit)
            case _:
                response_error = {"Error": f"pipeline must be in {pipeline}"}
                responses.append(response_error)
    
    return {
        "responses": responses
    }
            