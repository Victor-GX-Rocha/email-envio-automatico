"""
Core models and abstractions for database operations.

Provides reusable components for:
- ORM base classes.
- Base converter implementations.

Classes:
    ConvertersBase: Base class for ORM-to-dataclass conversions.

TypeVars:
    DataclassTable: Represents a dataclass model.
    ORMTable: Represents an ORM model entity.
"""


from typing import TypeVar

DataclassTable = TypeVar("DataclassTable") # Represents a dataclass model used for business logic.
ORMTable = TypeVar("ORMTable") # Represents an ORM model mapped to database tables.


class ConvertersBase:
    """
    Base class for converting between ORM entities and dataclasses.
    
    Subclasses must implement the `orm_convert` method for specific type conversion.
    """
    def __init__(self, orm_table: ORMTable):
        """
        Initialize converter for a specific ORM type.
        
        Args:
            orm_table: The ORM model class to convert from
        """
        self.orm_table = orm_table
    
    def convert(
            self, 
            orm_objs: list[ORMTable] | ORMTable
        ) -> list[ORMTable] | DataclassTable:
        """
        Convert ORM entities to dataclass objects.
        
        Handles both single entities and collections.
        
        Args:
            orm_objs: Single ORM entity or list of entities.
        
        Returns:
            Matching dataclass object or list of objects.
        
        Raises:
            TypeError: For unsupported input types.
        
        Example:
            >>> converter.convert(single_entity)
            DataclassTable(...)
            >>> converter.convert([entity1, entity2])
            [DataclassTable(...), DataclassTable(...)]
        """
        if type(orm_objs) == self.orm_table:
            return self.orm_convert(orm_objs)
        elif type(orm_objs) == list:
            return self.orms_convert(orm_objs)
        else:
            raise TypeError(f"[{self.__class__.__name__}] Formato de dado inválido: {type(orm_objs)}")
    
    def orm_convert(self, orm_obj: ORMTable) -> DataclassTable:
        """
        Convert a single ORM entity to dataclass (MUST be implemented by subclass).
        
        Args:
            orm_obj (ORMTable): A single ORM entity.
        
        Returns:
            DataclassTable: Converted dataclass instance.
        
        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses devem implementar esse método.")
    
    def orms_convert(self, orm_objs: list[ORMTable]) -> list[DataclassTable]:
        """
        Convert multiple ORM entities to dataclasses.
        
        Args:
            orm_objs (list[ORMTable]): List of ORM entities
        
        Returns:
            list[DataclassTable]: List of converted dataclass instances
        """
        return [self.orm_convert(orm_obj) for orm_obj in orm_objs]
