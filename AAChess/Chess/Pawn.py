from .Piece import Piece
from .Position import Position


class Pawn(Piece):
    def __init__(self, color:str, name:str, game_id:int,first_move=True,moved_by_two=False,made_first_move=False)->None:
        self.__first_move = first_move
        self.__moved_by_two = moved_by_two
        self.__made_first_move = made_first_move
        super().__init__(color, name, game_id)
        
        

    def code(self) -> str:
        return self.color[0].lower() + self.name[0].upper() + str(self.id) 
    
    def can_move(self, start: Position, end: Position, piece_color:str) -> bool:
        row_diff = end.row - start.row
        col_diff = abs(end.column - start.column)
    
        if self.__first_move:
            if abs(row_diff) == 2 and col_diff == 0:
                self.__moved_by_two = True
                return True
    
        if row_diff == 1 and col_diff == 0 and piece_color == 'black':
            return True
        elif row_diff == -1 and col_diff == 0 and piece_color == 'white':
            return True
        return False
    
    @property
    def first_move(self)->bool:
        return self.__first_move
    @first_move.setter
    def first_move(self, new_value:bool)->None:
        self.__first_move = new_value

    @property
    def made_first_move(self)->bool:
        return self.__made_first_move
    @made_first_move.setter
    def made_first_move(self, new_value:bool)->None:
        self.__made_first_move = new_value

    @property
    def moved_by_two(self)->bool:
        return self.__moved_by_two
    @moved_by_two.setter
    def moved_by_two(self, new_value:bool)->None:
        self.__moved_by_two = new_value

    def copy_pawn(self):
        return Pawn(self.color, self.name, self.id,self.__first_move,self.__moved_by_two,self.made_first_move)  