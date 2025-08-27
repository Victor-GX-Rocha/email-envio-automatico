"""
CRUD repositories for tables.

Provides:
    EmailRepository: Repository for table email.
"""

from .email.email import EmailRepository

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    "EmailRepository"
]
