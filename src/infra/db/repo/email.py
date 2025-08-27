""" Repository for table email. """

from datetime import datetime, date
from src.infra.db.models.email import Email, EmailConverter, EmailRecord
from src.infra.db.repo.session.session_manager import session_scope
from .models import ResponseCode
from .base import (
    # BaseGetMethods,
    BaseUpdateMethods,
    BaseDeleteMethods,
    BaseInsertMethods
)

class EmailGetMethods:
    def __init__(self):
        self.converter = EmailConverter()
    
    def by_column_value(self, operacao: int) -> list[EmailRecord]:
        """
        Pick all lines with specified `operacao` value.
        
        Args:
            operacao (int): Number of operation type.
        Returns:
            (list[EmailRecord]): list of a EmailRecord objects. (Empty list if it not exists).
        """
        with session_scope() as session:
            operations = session.query(Email).filter(Email.cod_retorno == operacao).all()
            return self.converter.convert(operations)
    
    def pending_operations(self) -> list[Email]:
        """ Get pending operations. """
        return self.by_column_value(ResponseCode.PENDING)
    
    def completed_operations(self) -> list[Email]:
        """ Get completed operations. """
        return self.by_column_value(ResponseCode.SUCCESS)
    
    def in_process_operations(self) -> list[Email]:
        """ Get in-process operations. """
        return self.by_column_value(ResponseCode.EXECUTING)


class EmailUpdateMethods(BaseUpdateMethods):
    def log_success(self, id: int) -> None:
        """ Register the result. """
        with session_scope() as session:
            line: Email = session.query(Email).get(id)
            line.dt_envio = date.today()
            line.hora_envio = datetime.now().time()
            line.cod_retorno = ResponseCode.SUCCESS

class EmailInsertMethods(BaseDeleteMethods):...
class EmailDeleteMethods(BaseInsertMethods):...

class EmailRepository:
    """ SQL commands for table email. """
    def __init__(self):
        self.get = EmailGetMethods()
        self.update = EmailUpdateMethods(Email)
        self.insert = EmailInsertMethods(Email)
        self.delete = EmailDeleteMethods(Email)
