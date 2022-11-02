from tortoise import Tortoise, run_async
from users.settings import USERS_DB


async def connect_to_db():
    await Tortoise.init(
        db_url=USERS_DB,
        modules={'models': ['db.models']}
    )


async def main():
    await connect_to_db()
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(main())
