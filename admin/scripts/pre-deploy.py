import asyncio


from portr_admin.db import connect_db, disconnect_db
from portr_admin.services.settings import populate_global_settings


async def main():
    await connect_db(generate_schemas=True)
    await populate_global_settings()
    await disconnect_db()


asyncio.run(main())