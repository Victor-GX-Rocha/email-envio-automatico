""" SQLAlchemy entity for table produtos_status. """

from typing import Optional
from datetime import date, time, datetime
from sqlalchemy import event, String, Integer, Text, Date, Time, ForeignKey, Sequence
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, composite
from sqlalchemy.schema import CreateSequence

from .data_class import EmailShippingDetails, EmailContent, EmailLog

class Base(DeclarativeBase):
    pass


class Email(Base):
    __tablename__ = "email"
    
    id_seq = Sequence("email_id_sq1")
    
    # id: Mapped[int] = mapped_column(Integer, primary_key=True, erver_default=id_seq.next_value())
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
    dt_envio: Mapped[Optional[date]] = mapped_column(Date, nullable=False)
    hora_envio: Mapped[Optional[time]] = mapped_column(Time, nullable=False)
    
    shipping_details = composite(
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
