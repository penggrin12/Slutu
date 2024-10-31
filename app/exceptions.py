from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from app.types import SlutuPlugin


class NoPluginConfiguration(NotImplementedError):
    def __init__(self, plugin: SlutuPlugin) -> None:
        super().__init__(f"A plugin ({str(plugin)}) cannot be loaded without proper configuration.")
