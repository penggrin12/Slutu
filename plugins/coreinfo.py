from typing import Self

from telethon.types import Message

from app import utils
from app.types import SlutuPlugin, SlutuPluginConfiguration


class CoreInfo(SlutuPlugin):
    async def on_config(self: Self) -> None:
        self.config = SlutuPluginConfiguration(
            new_messages_receive_direction=SlutuPluginConfiguration.ReceiveDirection.OUTGOING
        )

    async def on_load(self: Self) -> None:
        pass

    async def on_message(self: Self, message: Message) -> None:
        self.logger.debug(message)

        if message.text.startswith(";info"):
            await utils.answer(
                message,
                html=f"Slutu {'.'.join(map(str, self.slutu.version))} [<code>{self.slutu.dirhash[:6]}</code>...]",
            )
