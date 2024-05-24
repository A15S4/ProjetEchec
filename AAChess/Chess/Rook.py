from .Piece import Piece
from .Position import Position

class Rook(Piece):
    def __init__(self, color:str, name:str, game_id:int,first_move=True)->None:
        super().__init__(color, name, game_id)
        self.__first_move = first_move


    def code(self) -> str:
        return self.color[0].lower() + self.name[0].upper() + str(self.id) 
    
    def can_move(self, start: Position, end: Position) -> bool:
        if start == end:
            return False 
        if start.row == end.row or start.column == end.column:
            if start != end:
                if self.__first_move:
                    self.__first_move = False
                return True
          
        return False
    
    @property
    def first_move(self)->bool:
        return self.__first_move
    
    @first_move.setter
    def first_move(self, new_value:bool)->None:
        self.__first_move = new_value

    def copy_rook(self):
        return Rook(self.color, self.name, self.id,self.__first_move)