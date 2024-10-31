from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Tuple
import checksumdir
from telethon import Client
import telethon
import telethon.events
from telethon.types import User

from app import utils
from app.dispatcher import Dispatcher
from app.loader import Loader


class Slutu:
    version: Tuple[int, int, int]
    client: Client
    loader: Loader
    dispatcher: Dispatcher
    logger: logging.Logger
    me: User

    def __init__(self) -> None:
        self.version = (0, 0, 1)
        self.dirhash: str = checksumdir.dirhash(
            Path(".") / Path("app"), excluded_extensions=["pyc"]
        )
        self.logger = utils.get_logger(self)
        self.client = Client(
            "slutu",
            api_id=19715841,
            api_hash="12bfb1de93286f5aac3a1589a995886c",
            # api_id=2040,
            # api_hash="b18441a1ff607e10a989891a5462e627",
            # device_model="Desktop",
            # system_version="Windows 10",
            # app_version="5.6.3 x64",
            # lang_code="en",
            # system_lang_code="en-US",
        )
        self.loader = Loader()
        self.loader.slutu = self
        self.dispatcher = Dispatcher()
        self.dispatcher.slutu = self
        self.dispatcher.loader = self.loader

    async def run(self) -> None:
        print(self.client)
        async with self.client:
            self.me = await self.client.interactive_login()

            await self.loader.load_plugins()

            async def p(*args, **kwargs) -> Any:
                return await self.dispatcher.on_message(*args, **kwargs)

            # @self.client.on(telethon.events.Raw)
            # async def d(event: telethon.events.Raw):
            #     print(event)

            # self.client.on(telethon.events.NewMessage)(p)
            self.client.add_event_handler(p, telethon.events.NewMessage)

            await self.client.run_until_disconnected()
