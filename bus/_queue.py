import asyncio

_event_queue = asyncio.Queue()

async def put(event):
    event = await _event_queue.put(event)
    return event

async def get():
    event = await _event_queue.get()
    return event

def task_done():
    _event_queue.task_done()
