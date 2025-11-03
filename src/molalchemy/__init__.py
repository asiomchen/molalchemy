from loguru import logger

from molalchemy._version import __version__

logger.disable("molalchemy")
__all__ = ["__version__"]
