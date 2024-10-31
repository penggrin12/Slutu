from __future__ import annotations

import logging
from pathlib import Path
from types import ModuleType
from typing import List, Self, TYPE_CHECKING
import importlib.machinery
import inspect
import sys

from app import types, utils
from app.exceptions import NoPluginConfiguration
from app.types import SlutuPlugin, SlutuPluginConfiguration

if TYPE_CHECKING:
    from app.app import Slutu


class Loader:
    plugins: List[SlutuPlugin]
    logger: logging.Logger
    slutu: Slutu

    def __init__(self: Self) -> None:
        self.logger = utils.get_logger(self)
        self.plugins = []

    async def load_plugin(self: Self, path: Path) -> SlutuPlugin:
        name: str = f"modules.{path.name.strip().split('.')[0]}"
        spec = importlib.machinery.ModuleSpec(
            name,
            types.StringLoader(path.read_text(encoding="utf-8")),
            origin=name,
        )

        module: ModuleType = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)

        plugin: SlutuPlugin = next(
            (
                value()
                for value in vars(module).values()
                if inspect.isclass(value)
                and issubclass(value, SlutuPlugin)
                and value != SlutuPlugin
            ),
            None,
        )

        plugin.is_core = path.name.startswith("core")
        plugin.loader = self
        plugin.slutu = self.slutu

        if hasattr(module, "__version__"):
            plugin.__version__ = module.__version__

        await plugin.on_config()

        if (not plugin.config) or (not isinstance(plugin.config, SlutuPluginConfiguration)):
            raise NoPluginConfiguration(plugin)

        await plugin.on_load()

        self.plugins.append(plugin)

        return plugin

    async def load_plugins(self: Self) -> None:
        for plugin_path in (Path(".") / Path("plugins")).iterdir():
            await self.load_plugin(plugin_path)
