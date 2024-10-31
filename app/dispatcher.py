from __future__ import annotations

import logging
import typing

from telethon.types import Message

from app import utils
from app.types import SlutuPluginConfiguration

if typing.TYPE_CHECKING:
    from app.app import Slutu
    from app.loader import Loader


class Dispatcher:
    slutu: Slutu
    loader: Loader
    logger: logging.Logger

    def __init__(self: typing.Self) -> None:
        self.logger = utils.get_logger(self)

    async def on_message(self: typing.Self, message: Message) -> None:
        self.logger.debug(f"Got message ({message.id} in {message.chat.id}).")

        message_direction: SlutuPluginConfiguration.ReceiveDirection = (
            SlutuPluginConfiguration.ReceiveDirection.OUTGOING
            if message.outgoing
            else SlutuPluginConfiguration.ReceiveDirection.INCOMING
        )

        # saved messages should count as outgoing
        if message.chat.id == self.slutu.me.id:
            message_direction = SlutuPluginConfiguration.ReceiveDirection.OUTGOING

        self.logger.debug(message_direction)

        for plugin in self.loader.plugins:
            try:
                self.logger.debug(plugin.config.new_messages_receive_direction)
                if (
                    plugin.config.new_messages_receive_direction
                    != SlutuPluginConfiguration.ReceiveDirection.BOTH
                ) and (plugin.config.new_messages_receive_direction != message_direction):
                    continue

                await plugin.on_message(message)
            except Exception as e:
                self.logger.exception(e)
