from .Piece import Piece

class Intersection:
    def __init__(self, piece:Piece = None)->None:
        self.__piece = piece
        
    @property
    def piece(self)->Piece:
        return self.__piece
    @piece.setter
    def piece (self, piece:Piece)->None:
        self.__piece = piece
        
    def is_occupied(self)->bool:
        return self.__piece is not None
        
    def same_color_occupation(self, color: str)->bool:
        return self.is_occupied() and self.__piece.color == color  