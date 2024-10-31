from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import logging
import typing
from importlib.abc import SourceLoader

from telethon.types import Message

from app import utils
from app.exceptions import NoPluginConfiguration

if typing.TYPE_CHECKING:
    from app.app import Loader, Slutu

__all__: typing.List[str] = [
    "StringLoader",
    "SlutuPlugin",
    "SlutuPluginConfiguration",
]


class StringLoader(SourceLoader):
    # source: https://stackoverflow.com/a/62492464
    # edits : type hinting

    data: str

    def __init__(self: typing.Self, data: str) -> None:
        self.data = data

    def get_source(self: typing.Self, fullname: str) -> str:
        return self.data

    def get_data(self: typing.Self, path: str) -> bytes:
        return self.data.encode("utf-8")

    def get_filename(self: typing.Self, fullname: str) -> str:
        return "<not a real path>/" + fullname + ".py"


@dataclass
class SlutuPluginConfiguration:
    class ReceiveDirection(Enum):
        INCOMING = 0
        BOTH = 1
        OUTGOING = 2

    new_messages_receive_direction: ReceiveDirection


class SlutuPlugin:
    config: SlutuPluginConfiguration
    logger: logging.Logger
    is_core: bool = False
    loader: Loader
    slutu: Slutu

    def __init__(self: typing.Self) -> None:
        self.logger = utils.get_logger(self)

    def __str__(self: typing.Self) -> str:
        return f"<{'Core ' if self.is_core else ''}Plugin '{self.__class__.__name__}'>"

    def __repr__(self: typing.Self) -> str:
        return str(self)

    async def on_config(self: typing.Self) -> None:
        raise NoPluginConfiguration(self)

    async def on_load(self: typing.Self) -> None:
        pass

    async def on_message(self: typing.Self, message: Message) -> None:
        pass
