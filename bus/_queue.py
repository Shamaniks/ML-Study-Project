import asyncio

_event_queue = asyncio.Queue()

async def put(event):
    await _event_queue.put(event)

async def get():
    await _event_queue.get()

def task_done():
    _event_queue.task_done()
