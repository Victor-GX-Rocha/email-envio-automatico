""" SQLAlchemy entity for table produtos_status. """

from typing import Optional
from datetime import date, time, datetime
from sqlalchemy import event, String, Integer, Text, Date, Time, ForeignKey, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite
from sqlalchemy.schema import CreateSequence

from .data_class import EmailRecord, EmailShippingDetails, EmailContent, EmailLog

class Base(DeclarativeBase):
    pass

import re

class Email(Base):
    __tablename__ = "email"
    
    id_seq = Sequence("email_id_sq1")
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        server_default=id_seq.next_value()
    )
    
    cnpj: Mapped[str] = mapped_column(String(32))
    cod_retorno: Mapped[int] = mapped_column(Integer, default=0)
    
    email_emitente: Mapped[str] = mapped_column(String(256))
    senha_email_emitente: Mapped[str] = mapped_column(String(256))
    smtp_emitente: Mapped[str] = mapped_column(String(128))
    email_destinatario: Mapped[str] = mapped_column(String(256))
    
    assunto: Mapped[str] = mapped_column(String(2058))
    mensagem: Mapped[Optional[str]] = mapped_column(Text)
    anexos: Mapped[Optional[str]] = mapped_column(Text)
    log_erro: Mapped[Optional[str]] = mapped_column(Text)
    
    dt_criacao: Mapped[date] = mapped_column(Date, default=date.today)
    hora_criacao: Mapped[time] = mapped_column(Time, default=datetime.now().time)
    dt_envio: Mapped[Optional[date]] = mapped_column(Date)
    hora_envio: Mapped[Optional[time]] = mapped_column(Time)
    
    shipping = composite(
        EmailShippingDetails,
        "email_emitente",
        "senha_email_emitente",
        "smtp_emitente",
        "email_destinatario",
        deferred=False
    )
    
    content = composite(
        EmailContent,
        "assunto",
        "mensagem",
        "anexos",
        "log_erro",
        deferred=False
    )
    
    log = composite(
        EmailLog,
        "dt_criacao",
        "hora_criacao",
        "dt_envio",
        "hora_envio",
        deferred=False
    )
    
    @classmethod
    def __declare_last__(cls):
        """ Create the sequence after create the table. """
        event.listen(
            target=cls.__table__,
            identifier="after_create",
            fn=CreateSequence(cls.id_seq)
        )
    
    def to_dataclass(self) -> EmailRecord:
        """ Convert the ORM table to a dataclass version. """
        
        shipping = self.shipping
        content = self.content
        
        shipping.recipient_email = re.split(r'[;,]', self.email_destinatario.strip()) if self.email_destinatario else None
        content.attachments = re.split(r'[,;]', self.anexos.strip()) if self.anexos else None
        
        return EmailRecord(
            id=self.id,
            cnpj=self.cnpj,
            cod_retorno=self.cod_retorno,
            shipping=shipping,
            content=self.content,
            log=self.log
        )
