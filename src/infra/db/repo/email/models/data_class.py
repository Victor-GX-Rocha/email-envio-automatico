""" Dataclass model for email table. """

from dataclasses import dataclass
from typing import Optional
from datetime import date, time


@dataclass
class EmailShippingDetails:
    """
    User data used to send the email.
    Args:
        sender_email (str): email_emitente column.
        sender_password (str): senha_email_emitente column.
        sender_smtp (str): smtp_emitente column.
        recipient_email (list[str]): email_destinatario column.
    """
    sender_email: str
    sender_password: str
    sender_smtp: str
    recipient_email: list[str]

@dataclass
class EmailContent:
    """
    Email contents.
    Args:
        subject (str): assunto column.
        message (Optional[str]): mensagem column.
        attachments (Optional[list[str]]): anexos column.
        error_message (Optional[str]): mensagem_erro column.
    """
    subject: str
    message: Optional[str] = None
    attachments: Optional[list[str]] = None
    error_message: Optional[str] = None

@dataclass
class EmailLog:
    """
    Time logs for each email.
    Args:
        creation_date (date): dt_criacao column.
        creation_time (time): hora_criacao column.
        sent_date (Optional[date]): dt_envio column.
        sent_time (Optional[time]): hora_envio column.
    """
    creation_date: date
    creation_time: time
    sent_date: Optional[date] = None
    sent_time: Optional[time] = None

@dataclass
class EmailRecord:
    """ Record of "email" table. """
    id: int
    cnpj: str
    cod_retorno: int
    shipping: EmailShippingDetails
    content: EmailContent
    log: EmailLog
