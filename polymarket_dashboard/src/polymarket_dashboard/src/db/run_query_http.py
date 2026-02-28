import requests
from polymarket_dashboard.src.config.types import Query


def execute_https_query(host: str, port: int | str, query: Query, logger) -> requests.Response:
    url = f"http://{host}:{port}/exec"
    try:
        response = requests.get(url, params={'query': query})
        response.raise_for_status()
        logger.info(f"Query executed successfully: {query} \t Response: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f'Error executing query: {e} \t Query: {query} \t Response: {response.text}')
        raise e
