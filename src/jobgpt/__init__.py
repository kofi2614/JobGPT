"""Top-level package for jobgpt."""
from importlib import metadata
from importlib.metadata import PackageNotFoundError

__all__ = ["__version__"]

__version__ = "DEV"
try:
    __version__ = metadata.version(__name__)
except PackageNotFoundError:
    pass