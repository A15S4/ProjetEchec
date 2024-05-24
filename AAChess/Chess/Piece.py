from abc import ABC, abstractmethod
from .Position import Position

class Piece(ABC):
    _piece_count = {}

    def __init__(self, color: str, name: str, id:int) -> None:
        self.__color: str = color
        self.__name: str = name
        self.__id: int = id
        self.__code: str = self.code()
   
    @abstractmethod
    def can_move(self, start: Position, end: Position) -> bool:
        pass

    @abstractmethod
    def code(self) -> str:
        pass

    @property
    def color(self) -> str:
        return self.__color

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> int:
        return self.__id

    @property
    def code(self) -> str:
        return self.__code
    
    def copy(self) -> 'Piece':
        return type(self)(self.__color, self.__name, self.__id)