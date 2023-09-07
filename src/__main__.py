import logging
import os
import typing as t
from pathlib import Path
from uuid import uuid4

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger("uvicorn")
app = FastAPI()
app.mount("/static", StaticFiles(directory=Path("static"), html=True), name="static")

ENV_ENDPOINT = str(uuid4())


@app.get(f"/{ENV_ENDPOINT}")
async def get_environment() -> t.Mapping[str, t.Any]:
    return os.environ


@app.get("/")
async def root():
    return RedirectResponse(url="/static")


@app.on_event("startup")
async def startup_event():
    logger.info(f"Environment endpoint available at {ENV_ENDPOINT}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
