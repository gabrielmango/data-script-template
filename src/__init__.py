"""Data Script Template - Template para scripts Python focados em ETL."""

__version__ = '0.1.0'
__author__ = 'gabrielhmango'

from src.db import MongoDBConnection, PostgresConnection
from src.pipeline import (
    DefaultETLPipeline,
    ETLPipeline,
    ExtractStep,
    LoadStep,
    TransformStep,
)
from src.utils import ConfigLoader, Logger

__all__ = [
    # Pipeline base classes
    'ExtractStep',
    'TransformStep',
    'LoadStep',
    'ETLPipeline',
    'DefaultETLPipeline',
    # Database connections
    'PostgresConnection',
    'MongoDBConnection',
    # Utilities
    'ConfigLoader',
    'Logger',
]
