from db import db
from bot.apps import *
import logging
import sys
import asyncio

async def create_all():
    await db.create_all()


if __name__ == "__main__":
#   loop = asyncio.get_event_loop()
#   loop.run_until_complete(create_all())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
