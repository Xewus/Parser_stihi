from fastapi import FastAPI

from app.routers.default_router import router as default_router
from app.routers.parsing import router as parsing_router
from app.core.settings import DEBUG, APP_NAME, APP_VERSION, APP_DESCRIPTION, AUTHOR

app = FastAPI(
    debug=DEBUG,
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=AUTHOR
)

app.include_router(router=default_router)
app.include_router(parsing_router)
