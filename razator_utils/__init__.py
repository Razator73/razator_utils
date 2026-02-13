"""Top-level package for Razator Utils."""

__author__ = """Ryan Scott"""
__email__ = 'ryan.t.scott73@gmail.com'
__version__ = '0.6.0'

from razator_utils.razator_utils import (
    batchify,
    camel_to_snake,
    flatten_dict,
    get_chrome_major_version,
    discord_message,
)
from razator_utils import log

__all__ = ['batchify', 'camel_to_snake', 'log', 'flatten_dict', 'get_chrome_major_version', 'discord_message']
