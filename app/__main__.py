from fastapi import FastAPI

from app.router import router

app = FastAPI(title="DBS")
app.include_router(router)
