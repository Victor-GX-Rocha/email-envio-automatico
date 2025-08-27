"""
Functionalities for table email.

Provides:
    Email: ORM class entity.
    EmailRecord: 
    EmailShippingDetails: 
    EmailContent: 
    EmailLog: 
    EmailConverter: Class converter.
"""

from .orm_entity import Email
from .data_class import EmailRecord, EmailShippingDetails, EmailContent, EmailLog
from .orm_converter import EmailConverter

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "Email",
    "EmailRecord", "EmailShippingDetails", "EmailContent", "EmailLog",
    "EmailConverter"
]
