import logging
from pathlib import Path

import checksumdir
from telethon.types import Message


def get_logger(cls: object) -> logging.Logger:
    return logging.getLogger(cls.__class__.__name__)


async def answer(message: Message, text: str = None, *args, **kwargs) -> Message:
    if message.chat.id == (await message._client.get_me()).id:
        return await message.edit(*args, text=text, **kwargs)
    return await message.reply(*args, text=text, **kwargs)


def get_app_hash() -> str:
    return checksumdir.dirhash(Path(".") / Path("app"), excluded_extensions=["pyc"])


def get_plugins_hash() -> str:
    return checksumdir.dirhash(Path(".") / Path("plugins"), excluded_extensions=["pyc"])

