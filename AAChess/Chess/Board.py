"""
Nom du fichier : Board.py
Contexte : Ce fichier contient la classe contenant l'implémentation d'un jeu d'échec.
Auteurs : Aissa Bouaraguia
"""

from .Intersection import Intersection
from .Pawn import Pawn
from .Rook import Rook
from .Bishop import Bishop
from .Knight import Knight
from .Queen import Queen
from .King import King
from .Position import Position
from .stack import Stack
import copy



class Board:
    def __init__(self)->None:
        self.__board:list[list[Intersection]] = [[],[],[],[],[],[],[],[]]
        self.start()
        self.__stack = Stack()
        self.__last_move = None
        self.__is_game_over = False
        self.__draw = False
        
    @property
    def board(self)->list:
        return self.__board
    
    @property
    def last_move(self):
        return self.__last_move
    
    @last_move.setter
    def last_move(self,value):
        self.__last_move = value

    @property
    def is_game_over(self):
        return self.__is_game_over
    
    @property
    def draw(self):
        return self.__draw
    
    @property
    def stack(self):
        return self.__stack

    def is_checkmate(self, color: str) -> bool:
        board = copy.deepcopy(self)
        all_legal_moves = board.get_all_legal_moves(color)
        if len(all_legal_moves) == 0:
            self.__is_game_over = True
            if not self.check_for_check(color):
                self.__draw = True
            return True
        else:
            return False
    
    def check_for_check(self, color):
        king_position = None
        for row in range(8):
            for col in range(8):
                intersection = self.get_intersection(row, col)
                if intersection.is_occupied() and isinstance(intersection.piece, King) and intersection.piece.color == color:
                    king_position = Position(row, col)
                    break
            if king_position:
                break
        if not king_position:
            return False
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                intersection = self.get_intersection(row, col)
                if intersection.is_occupied() and intersection.piece.color == opponent_color:
                    piece_position = Position(row, col)
                    if self.path_is_possible(piece_position, king_position):
                        return True
        return False
    
    def start(self)->None:
        for i in range(8):
            self.__board[2].append(Intersection(None))
            self.__board[3].append(Intersection(None))
            self.__board[4].append(Intersection(None))
            self.__board[5].append(Intersection(None))

        self.__board[0].append( Intersection(Rook  ("black", "rook"  , 1)))
        self.__board[0].append( Intersection(Knight("black", "knight", 1)))
        self.__board[0].append( Intersection(Bishop("black", "bishop", 1)))
        self.__board[0].append( Intersection(Queen ("black", "queen" , 1)))
        self.__board[0].append( Intersection(King  ("black", "king"  , 1)))
        self.__board[0].append( Intersection(Bishop("black", "bishop", 2)))
        self.__board[0].append( Intersection(Knight("black", "knight", 2)))
        self.__board[0].append( Intersection(Rook  ("black", "rook"  , 2)))
    
        self.__board[1].append( Intersection(Pawn("black", "pawn", 1)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 2)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 3)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 4)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 5)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 6)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 7)))
        self.__board[1].append( Intersection(Pawn("black", "pawn", 8)))
    
        self.__board[6].append( Intersection(Pawn("white", "pawn", 1)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 2)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 3)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 4)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 5)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 6)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 7)))
        self.__board[6].append( Intersection(Pawn("white", "pawn", 8)))
    
        self.__board[7].append( Intersection(Rook  ("white", "rook"  , 1)))
        self.__board[7].append( Intersection(Knight("white", "knight", 1)))
        self.__board[7].append( Intersection(Bishop("white", "bishop", 1)))
        self.__board[7].append( Intersection(Queen ("white", "queen" , 1)))
        self.__board[7].append( Intersection(King  ("white", "king"  , 1)))
        self.__board[7].append( Intersection(Bishop("white", "bishop", 2)))
        self.__board[7].append( Intersection(Knight("white", "knight", 2)))
        self.__board[7].append( Intersection(Rook  ("white", "rook"  , 2)))
            
    def board_json(self)->list[list[str]]:
        board_json = []
        for row in self.__board:
            for column in row:
                if column.piece == None:
                    board_json.append("")
                else:
                    board_json.append(column.piece.code())

        return board_json
                
    def get_intersection(self, row:int, col:int)->Intersection:
        return self.__board[row][col]
        
    def path_is_possible(self, start:Position, end:Position)->bool:
        row_diff = abs(end.row - start.row)
        col_diff = abs(end.column - start.column)
        start_intersection = self.get_intersection(start.row,start.column)
        end_intersection = self.get_intersection(end.row,end.column)

        if row_diff == 0 and col_diff == 0:
            return False
        
        if row_diff != 0 or col_diff != 0:
            if end_intersection.same_color_occupation(start_intersection.piece.color):
                return False

        if isinstance(start_intersection.piece, Pawn):
            return self.__pawn_path(start, end)
           
        elif isinstance(start_intersection.piece, Rook):
            return self.__rook_path(start, end) 
         
        elif isinstance(start_intersection.piece, Knight):
            return self.__knight_path(start, end)
        
        elif isinstance(start_intersection.piece, Bishop):
            return self.__bishop_path(start, end)
        
        elif isinstance(start_intersection.piece, Queen):
            return self.__queen_path(start, end)
        
        elif isinstance(start_intersection.piece, King):
            return self.__king_path(start, end)
        
        return self.__all_paths(start, end)
    
    def __all_paths(self, start: Position, end: Position) -> bool:
        if start.column == end.column:
            step = 1 if start.row < end.row else -1
            for i in range(start.row + step, end.row, step):
                if self.get_intersection(i,start.column).is_occupied():
                    return False
        elif start.row == end.row:
            step = 1 if start.column < end.column else -1
            for i in range(start.column + step, end.column, step):
                if self.get_intersection(start.row,i).is_occupied():
                    return False
        else:
            row_offset = 1 if end.row > start.row else -1
            col_offset = 1 if end.column > start.column else -1

            i, j = start.row + row_offset, start.column + col_offset
            while i != end.row and j != end.column:
                if self.get_intersection(i,j).is_occupied():
                    return False
                i += row_offset
                j += col_offset

        return True
        
    def __knight_path(self, start:Position, end:Position)->bool:
       return self.get_intersection(start.row,start.column).piece.can_move(start, end)
    
    def __pawn_path(self, start:Position, end:Position)->bool:
        row_diff = end.row - start.row
        col_diff = abs(end.column - start.column)
        piece = self.get_intersection(start.row,start.column).piece
        piece_color = piece.color
        result = False
        enemy_position=None

        if self.__last_move is not None:
            if isinstance(self.get_intersection(self.__last_move[1].row, self.__last_move[1].column).piece, Pawn):
                if abs(self.__last_move[1].row - self.__last_move[0].row) == 2:
                    enemy_position = self.__en_passant_possible(start, piece_color)

        if col_diff == 1 and row_diff == -1 and piece_color == "white":
            result = self._capture(start, end, enemy_position)

        elif col_diff == 1 and row_diff == 1 and piece_color == "black":
            result = self._capture(start, end, enemy_position)

        
        if self.__all_paths(start, end):
            if piece.can_move(start, end, piece_color):
                if self.__board[end.row][end.column].is_occupied():
                    return False
                if piece.first_move:
                    piece.first_move = False
                    piece.made_first_move = True
                result = True
        return result

    def _capture(self, start:Position, end:Position, enemy_position:tuple[Position,Position]):
        start_intersection = self.get_intersection(start.row,start.column)
        end_intersection = self.get_intersection(end.row,end.column)
        if enemy_position:
            row, col = enemy_position[0], enemy_position[1]
            if end.column == col:
                self.get_intersection(row,col).piece = None
                return True
        elif end_intersection.is_occupied() and end_intersection.same_color_occupation(start_intersection.piece.color):
            return False
        elif not end_intersection.is_occupied():
            return False
        elif end_intersection.is_occupied() and not end_intersection.same_color_occupation(start_intersection.piece.color):
            return True
        return False
    
    def __en_passant_possible(self, start: Position, color: str) -> bool | tuple:
        opposite_piece_color = "white" if color == "black" else "black"

        def check_side(start, column_offset):
            for offset in [column_offset, -column_offset]:
                if 0 <= start.column + offset < 8:
                    side_position = self.get_intersection(start.row,start.column + offset)
                    if side_position is not None and isinstance(side_position.piece, Pawn):
                        if side_position.piece.color == opposite_piece_color and side_position.piece.moved_by_two:
                            return (start.row, start.column + offset)

        side_position = check_side(start, 1)
        return side_position

        
    def __rook_path(self, start:Position, end:Position)->bool:
        if self.__all_paths(start, end):
            return self.get_intersection(start.row,start.column).piece.can_move(start, end)
            
    def __bishop_path(self, start:Position, end:Position)->bool:    
        if self.__all_paths(start, end):
            return self.get_intersection(start.row,start.column).piece.can_move(start, end)
        
    def __queen_path(self, start:Position, end:Position)->bool:
        if self.__all_paths(start, end):
            return self.get_intersection(start.row,start.column).piece.can_move(start, end)
        
    def __king_path(self, start:Position, end:Position)->bool:
        if self.__all_paths(start, end):
            return self.get_intersection(start.row,start.column).piece.can_move(start, end)
                
           
    
    def __castle_move(self, start: Position, end: Position) -> bool:
        is_kingside = end.column - start.column > 0
        start_intersection = self.get_intersection(start.row,start.column)
        end_intersection = self.get_intersection(end.row,end.column)

        if start_intersection.piece.color == "white":
            rook_column = 7 if is_kingside else 0
            rook_end_column = 5 if is_kingside else 3
            king_row = 7
        else:
            rook_column = 7 if is_kingside else 0
            rook_end_column = 5 if is_kingside else 3
            king_row = 0

        rook = self.get_intersection(king_row,rook_column).piece
        if isinstance(rook, Rook) and rook.first_move:
            if all(not self.get_intersection(king_row,col).is_occupied() for col in range(rook_column + 1, end.column)):
                end_intersection.piece = start_intersection.piece
                start_intersection.piece = None
                self.get_intersection(king_row,rook_end_column).piece = rook
                self.get_intersection(king_row,rook_column).piece = None
                return True
        return False
    
    def new_queen_id(self,color:str)->int:
        board = self.board_json()
        total = 0
        for i in board:
            if len(i) > 0 and i[0] == color[0] and i[1] == "Q":
                total += 1
        return total+1

    def move(self, start:Position, end:Position)->bool:
        if (self.path_is_possible(start, end)):
            if isinstance(self.get_intersection(start.row,start.column).piece, King) and abs(start.column - end.column) == 2:
                return self.__castle_move(start, end)
            
            start_position_piece = self.get_intersection(start.row,start.column).piece
            self.get_intersection(end.row, end.column).piece = start_position_piece
            self.__board[start.row][start.column].piece = None
            end_position_piece = self.get_intersection(end.row, end.column).piece

            if isinstance(end_position_piece, Pawn):
                if (end_position_piece.color == 'white' and end.row == 0) or (end_position_piece.color == 'black' and end.row == 7):
                        self.get_intersection(end.row, end.column).piece = Queen(end_position_piece.color, "queen", self.new_queen_id(end_position_piece.color))  
            if self.__last_move:
                if isinstance(self.get_intersection(self.__last_move[1].row, self.__last_move[1].column ).piece, Pawn):
                    self.get_intersection(self.__last_move[1].row,self.__last_move[1].column).piece.moved_by_two = False
            return True
        return False

    def pre_move(self, start: Position, end: Position):
        color = self.get_intersection(start.row, start.column).piece.color
        copied_board = Board.copy_board(self)
        self.__stack.push(copied_board)
        a = self.move(start, end)
        if not a:
            self.undo()
            return False
        
        if self.check_for_check(color):
            self.undo()
            return False
        
        self.undo()  
        return self.move(start, end) 
    
    def get_all_legal_moves(self,color) -> list[tuple[Position, Position]]:
        legal_moves = []
        for row in range(8):
            for col in range(8):
                intersection = self.get_intersection(row, col)
                if intersection.is_occupied() and intersection.piece.color == color:
                    piece_position = Position(row, col)
                    possible_moves = self.get_legal_moves_for_piece(piece_position)
                    legal_moves.extend(possible_moves)
        return legal_moves

    def get_legal_moves_for_piece(self, start_position) -> list[tuple[Position, Position]]:
        legal_moves = []
        for dest_row in range(8):
            for dest_col in range(8):
                dest_position = Position(dest_row, dest_col)
                self.__stack.push(Board.copy_board(self))
                if self.pre_move(start_position, dest_position):
                    legal_moves.append((start_position, dest_position))
                self.undo()
        return legal_moves
        
    def undo(self):
        self.__board = self.__stack.pop()

    @staticmethod
    def copy_board(board:'Board'):
        copied_board = []
        for i in range(8):
            row = []
            for j in range(8):
                intersection = board.get_intersection(i, j)
                piece = intersection.piece
                if piece is not None:
                    if isinstance(piece, King):
                        row.append(Intersection(piece.copy_king()))
                    elif isinstance(piece, Rook):
                        row.append(Intersection(piece.copy_rook()))
                    elif isinstance(piece, Pawn):
                        row.append(Intersection(piece.copy_pawn()))
                    else:
                        row.append(Intersection(piece.copy()))
                else:
                    row.append(Intersection(None))
            copied_board.append(row)
        return copied_board
    
    @staticmethod
    def last_move_copy(last_move:tuple[Position,Position]) -> tuple[Position,Position]:
        copied_move = tuple(last_move)
        return copied_move