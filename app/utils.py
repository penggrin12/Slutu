import logging
from pathlib import Path
from typing import List, Union

import checksumdir
from telethon.types import Message, File


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


async def get_file(message: Message) -> Union[File, None]:
    if message.file:
        return message.file
    if message.replied_message_id:
        replied_to: Message = await message.get_replied_message()
        return await get_file(replied_to)  # NOTICE: possible to be a reaaallyyy long recursion
    return None  # explicit None


def get_args_raw(message: Message) -> str:
    if " " not in message.text_html:
        return ""
    return message.text_html.split(" ", 1)[-1]


def get_args(message: Message) -> List[str]:
    args_raw: str = get_args_raw(message)
    if not args_raw:
        return []
    return args_raw.split(" ")
