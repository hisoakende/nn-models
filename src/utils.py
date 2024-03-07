import asyncio
from typing import Iterable


async def cancel_async_tasks(tasks: Iterable[asyncio.Task[None]]) -> None:
    for task in tasks:
        task.cancel()

    for task in tasks:
        try:
            await task
        except Exception:
            pass
        except asyncio.CancelledError:
            pass
