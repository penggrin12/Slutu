from pathlib import Path
from typing import Self

from telethon.types import Message

from app import utils
from app.types import SlutuPlugin, SlutuPluginConfiguration


class CoreLoader(SlutuPlugin):
    async def on_config(self: Self) -> None:
        self.config = SlutuPluginConfiguration(
            new_messages_receive_direction=SlutuPluginConfiguration.ReceiveDirection.OUTGOING
        )

    async def on_load(self: Self) -> None:
        pass

    async def on_message(self: Self, message: Message) -> None:
        if not message.text.startswith(";install"):
            return

        file = await utils.get_file(message)

        if not file:
            await utils.answer(message, "file not found")
            return

        plugin_path: Path = Path(".") / Path("plugins") / Path(Path(file.name).stem + ".py")

        await file.download(plugin_path)

        plugin: SlutuPlugin = await self.loader.load_plugin(plugin_path)

        await utils.answer(
            message, f"hopefully installed a new plugin. ({plugin.__class__.__name__})"
        )
