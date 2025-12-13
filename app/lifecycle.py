import asyncio
from workers.dispatcher import dispatcher

def setup_background_tasks(application):
    asyncio.create_task(dispatcher(application))
