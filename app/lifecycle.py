import asyncio
from workers.dispatcher import dispatcher

async def on_startup(application):
    asyncio.create_task(dispatcher(application))
