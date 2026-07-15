from utils.db import get_all_ratios

print(get_all_ratios)
from utils.db import (
    get_market_cap,
    get_peer_percentiles
)

print(get_market_cap().head())

print(get_peer_percentiles().head())

print("\nDatabase utilities tested successfully.")