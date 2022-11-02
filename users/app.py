from users.db.connect_to_db import connect_to_db
from tortoise import run_async
from tortoise.contrib.fastapi import register_tortoise

from fastapi import FastAPI


from users.api.router import router as users_router

app = FastAPI(
    debug=1,
    title='SimpleUsers',
    version='0.1.0'
)


app.include_router(
    router=users_router,
    prefix='/users'
)

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['users.db.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
# @app.on_event('startup')
# async def startup():
#     run_async(main())
