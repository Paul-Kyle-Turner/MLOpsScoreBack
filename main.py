
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    login_router,
    platform_router,
    score_router,
)


app = FastAPI()

app.include_router(login_router)
app.include_router(platform_router)
app.include_router(score_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
