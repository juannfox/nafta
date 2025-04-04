"""
API main
"""
import logging
from os import getenv

import client
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, Response

# Logging options
LOG_LEVEL = "DEBUG" if getenv("DEBUG") == "1" else "INFO"
logging.basicConfig(level=LOG_LEVEL)
# Globals
FAVICON = "../media/nafta.ico"
PORT = 8081

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


@app.get("/naftasuper")
async def naftasuper():
    """Get regular gas price"""
    df = source.get_gas_prices_dataframe()
    price = client.get_gas_price_avg(df, 2, "CAPITAL FEDERAL")
    return {"Nafta super": round(price, 2)}


# Init
if __name__ == "__main__":
    # Uvicorn server setup
    config = uvicorn.Config("main:app", port=PORT, log_level=LOG_LEVEL.lower())
    server = uvicorn.Server(config)
    server.run()
