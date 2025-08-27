""" Base common update functionalities. """

from src.infra.db.repo.session import session_scope
from src.infra.db.repo.models import ResponseCode


class Loggers:
    """ Basic common logers for any table who contains the cod_retorno, log_erro columns"""
    def log_error(self, id: int, cod_retorno: int, log_erro: str) -> None:
        """
        Log an error inside an especifiedy line.
        Args:
            id (int): Line ID.
            cod_retorno (int): Error code.
            log_erro (str): Log message.
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = cod_retorno
            line.log_erro = str(log_erro)
    
    def log_success_code(self, id: int, cod_retorno: int = ResponseCode.SUCCESS) -> None:
        """
        Log a simple message with the code sucess.
        Args:
            id (int): Line ID.
            cod_retorno (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = cod_retorno
    
    def got_to_sleep(self, id: int, cod_retorno: int = ResponseCode.SUCCESS) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            cod_retorno (int): Code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = cod_retorno
    
    def executing(self, id: int, cod_retorno: int = ResponseCode.EXECUTING) -> None:
        """
        Change the status operation to another number to make it "sleep"
        Args:
            id (int): Line ID.
            cod_retorno (int): Success code number. 
        """
        with session_scope() as session:
            line = session.query(self.entity).get(id)
            line.cod_retorno = cod_retorno
