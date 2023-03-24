"""
Python code for the API
"""
import logging
from os import getenv

import client

# Logging options
LOG_LEVEL = "DEBUG" if getenv("DEBUG") == "1" else "INFO"
logging.basicConfig(level=LOG_LEVEL)


gov = client.APIGobierno()
df = gov.get_gas_prices_dataframe()
price = client.get_gas_price_avg(df,2,"CAPITAL FEDERAL")
print(price)