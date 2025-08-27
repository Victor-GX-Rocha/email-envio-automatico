"""
Base shared CRUD commands for tables

Provides:
    BaseGetMethods: 
    BaseUpdateMethods: 
    BaseDeleteMethods: 
    BaseInsertMethods: 
"""

from .base import (
    BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "BaseGetMethods",
    "BaseUpdateMethods",
    "BaseDeleteMethods",
    "BaseInsertMethods",
]
