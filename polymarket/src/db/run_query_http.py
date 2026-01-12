import requests
from polymarket.src.config.types import Query


def execute_https_query(host: str, port: int | str, query: Query) -> requests.Response:
    url = f"http://{host}:{port}/exec"
    try:
        response = requests.get(url, params={'query': query})
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        raise e
