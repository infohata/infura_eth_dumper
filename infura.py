import os, requests, json
from dotenv import load_dotenv
from typing import Any

load_dotenv()

INFURA_NETWORK = os.getenv('INFURA_NETWORK', 'mainnet')
INFURA_API_KEY = os.getenv('INFURA_API_KEY', '')
url = f'https://{INFURA_NETWORK}.infura.io/v3/{INFURA_API_KEY}'
headers = {'content-type': 'application/json'}

def post(method: str, params: list[Any] = [], url: str = url, headers: dict[str, Any] = headers, **kwargs) -> dict[str, Any]:
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    payload.update(kwargs)
    response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    return response
