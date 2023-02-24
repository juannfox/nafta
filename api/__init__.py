"""
Python code for the API
"""
import logging
from os import getenv

import clientapi as client

# Logging options
log_level = "DEBUG" if getenv("DEBUG") == "1" else "INFO"
logging.basicConfig(level=log_level)


gov = client.APIGobierno()
print(gov.get_dataset_metadata())
response = gov.get_gas_prices_resource()
print(response.content)
