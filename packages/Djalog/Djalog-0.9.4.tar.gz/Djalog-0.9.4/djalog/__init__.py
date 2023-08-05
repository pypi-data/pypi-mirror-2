"""
Simple, Django-ready (but can be used without Django as well) logger
using excellent logging module.
"""
import logging

from djalog.conf import configure
from djalog.loggers import DjalogLogger

VERSION = (0, 9, 4, 'stable')

def get_version(version_tuple):
    last = version_tuple[-1]
    if isinstance(last, str) and last not in map(str.lower, ['alpha', 'beta']):
        version_tuple = version_tuple[:-1]
    return '.'.join(map(str, version_tuple))

__version__ = get_version(VERSION)

__all__ = ['configure', 'DjalogLogger', 'DjalogError']

configure()

def get_version():
    return __version__

