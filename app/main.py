import asyncio
from typing import NoReturn

from app.app import Slutu


def main() -> NoReturn:
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    loop.run_until_complete(amain())


async def amain() -> NoReturn:
    try:
        await Slutu().run()
    except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
        print("interrupted")
