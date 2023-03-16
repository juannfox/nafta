"""
Test
"""
import logging
from os import getenv

import client
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, Response

# Logging options
LOG_LEVEL = "DEBUG" if getenv("DEBUG") == "1" else "INFO"
logging.basicConfig(level=LOG_LEVEL)
# Globals
FAVICON = "../images/nafta.ico"

# Instantiations
source = client.APIGobierno()
app = FastAPI()


@app.get("/")
async def root():
    """Root msg"""
    return {"message": "This is Nafta API 0.0.1"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Website favicon"""
    return FileResponse(FAVICON)


@app.get("/doc", include_in_schema=False)
async def doc():
    """Redirection to Swagger Docs"""
    return RedirectResponse("/docs", 302)


@app.get("/metadata")
async def metadata():
    """Fetch Dataset Metadata"""
    return source.get_dataset_metadata()


@app.get("/dataset_url")
async def dataset_url():
    """Fetch Dataset file URL"""
    return source.datset_url()


@app.get("/dataset")
async def dataset():
    """Fetch Dataset file"""
    file = "tmp-datasource.csv"
    downloaded = source.get_gas_prices_resource_file(file)
    if downloaded:
        response = FileResponse(file)
    else:
        response = Response("Not found", 404)
    return response
