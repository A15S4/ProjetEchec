from .Piece import Piece
from .Position import Position

class Queen(Piece):
    def __init__(self, color:str, name:str, game_id:int)->None:
        super().__init__(color, name, game_id)


    def code(self) -> str:
        return self.color[0].lower() + self.name[0].upper() + str(self.id) 
    
    def can_move(self, start: Position, end: Position) -> bool:
        row_diff = abs(start.row - end.row)
        col_diff = abs(start.column - end.column)

        return (start.row == end.row or start.column == end.column or row_diff == col_diff)