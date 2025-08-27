""" Convert the ProdutosStatusORM entity to a Product dataclass object. """

from src.infra.db.models.bases import ConvertersBase
from .data_class import EmailRecord
from .orm_entity import Email


class EmailConverter(ConvertersBase):
    """ Provides conversion methods to transform a ProdutosStatusORM into ProdutosStatusDataclass. """
    def __init__(self):
        super().__init__(Email)
    
    def orm_convert(self, orm_obj: Email) -> EmailRecord:
        """
        Convert a single Produtos ORM entity to a Product dataclass.
        
        Args:
            orm_obj (Produtos): A single Produtos ORM entity.
        Returns:
            Product: Converted dataclass to instance.
        """
        return EmailRecord(
            id=orm_obj.id,
            cnpj=orm_obj.cnpj,
            cod_retorno=orm_obj.cod_retorno,
            shipping_details=orm_obj.shipping_details,
            content=orm_obj.content,
            log=orm_obj.log
        )
