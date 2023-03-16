"""
Test
"""
from fastapi import FastAPI
from fastapi.responses import FileResponse

FAVICON = "../images/nafta.ico"

app = FastAPI()

@app.get("/")
async def root():
    """Hello world"""
    return {"message": "Hello World"}


@app.get("/favicon.ico" , include_in_schema=False)
async def favicon():
    """Website favicon"""
    return FileResponse(FAVICON)
