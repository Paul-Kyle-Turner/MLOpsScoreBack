
from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get("/")
async def get_root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
