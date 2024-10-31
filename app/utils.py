import logging

from telethon.types import Message


def get_logger(cls: object) -> logging.Logger:
    return logging.getLogger(cls.__class__.__name__)


async def answer(message: Message, text: str = None, *args, **kwargs) -> Message:
    if message.chat.id == (await message._client.get_me()).id:
        return await message.edit(*args, text=text, **kwargs)
    return await message.reply(*args, text=text, **kwargs)
