from fastapi import FastAPI

from app.routers.main_router import main_router

app = FastAPI()

app.include_router(router=main_router)
