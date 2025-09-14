import asyncio
from asyncio import Future


def timeout_future(timeout=None) -> Future:
    fut = asyncio.get_event_loop().create_future()
    if timeout:
        return asyncio.wait_for(fut, timeout)
    return fut
