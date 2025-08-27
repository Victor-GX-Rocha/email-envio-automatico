"""
Models and constants for Repositories.

Provides:
    DataclassTable: Represents a dataclass model.
    ORMTable: Represents an ORM model entity.
    ResponseCode: Model with internal process response status.
"""

from typing import TypeVar

ORMTable = TypeVar("ORMTable") # Represents an ORM model mapped to database tables.
TableEntity = TypeVar("TableEntity") # Represents an ORM table entity.
DataclassTable = TypeVar("DataclassTable") # Represents a dataclass model used for business logic.

class ResponseCode:
    """
    Code response status.
    Args:
        PENDING (int): Operation was not started yet.
        EXECUTING (int): Operation is running.
        SUCCESS (int): Operation was performed successfully.
        NOT_FOUND (int): Data not found (likely 404 http response).
        TABLE_ERROR (int): Errors that occurred on the database (outside the program).
        PROGRAM_ERROR (int): Internal process errors (inside the program).
    """
    PENDING: int = 0
    EXECUTING: int = 1
    SUCCESS: int = 2
    
    NOT_FOUND: int = 3
    TABLE_ERROR: int = 88
    PROGRAM_ERROR: int = 91
