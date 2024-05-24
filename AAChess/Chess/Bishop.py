from .Piece import Piece
from .Position import Position

class Bishop(Piece):
    def __init__(self, color:str, name:str, game_id:int)->None:
        super().__init__(color, name, game_id)

    def code(self) -> str:
        return self.color[0].lower() + self.name[0].upper() + str(self.id) # ex: 'wK1'
    
    def can_move(self, start: Position, end: Position) -> bool:
        row_diff = abs(start.row - end.row)
        col_diff = abs(start.column - end.column)
        
        if start == end:
            return False
        
        return row_diff == col_diff