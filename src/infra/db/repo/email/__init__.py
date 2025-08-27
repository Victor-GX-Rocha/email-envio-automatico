"""
Functionalities for table email.

Provides:
    Email: ORM class entity.
    EmailRecord: 
    EmailShippingDetails: 
    EmailContent: 
    EmailLog: 
"""

from .models.orm_entity import Email
from .models.data_class import EmailRecord, EmailShippingDetails, EmailContent, EmailLog

__version__ = "v.0.0.1"
__all__ = [
    "__version__",
    
    "Email",
    "EmailRecord", "EmailShippingDetails", "EmailContent", "EmailLog",
]
