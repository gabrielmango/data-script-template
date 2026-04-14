"""Data Script Template - Template para scripts Python focados em ETL."""

__version__ = '0.1.0'
__author__ = 'gabrielhmango'

from src.db import MongoDBConnection, PostgresConnection
from src.pipeline import extract, load, transform
from src.utils import ConfigLoader, Logger

__all__ = [
    # Pipeline functions
    'extract',
    'transform',
    'load',
    # Database connections
    'PostgresConnection',
    'MongoDBConnection',
    # Utilities
    'ConfigLoader',
    'Logger',
]
