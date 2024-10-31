from logging import basicConfig
import logging


def setup() -> None:
    basicConfig(level=logging.DEBUG)
