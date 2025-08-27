"""
Functionalities for table email.

Provides:
    Email: ORM class entity.
    EmailRecord: A dataclass model to represents the entirely email table.
    EmailShippingDetails: Represents the shipping info clumns from email table.
    EmailContent: Represents the content columns from email table.
    EmailLog: Represents the log columns from email table.
"""

from .orm_entity import Email
from .data_class import EmailRecord, EmailShippingDetails, EmailContent, EmailLog

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "Email",
    "EmailRecord", "EmailShippingDetails", "EmailContent", "EmailLog",
]
