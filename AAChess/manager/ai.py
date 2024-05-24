import random
from ..Chess.Piece import Piece
from ..Chess.Bishop import Bishop
from ..Chess.Rook import Rook
from ..Chess.Knight import Knight
from ..Chess.Queen import Queen
from ..Chess.King import King
from ..Chess.Pawn import Pawn
from ..Chess.Board import Board
from ..Chess.Position import Position
from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def evaluate_board(self, board)->int:
        pass

    @abstractmethod
    def best_move(self, board, depth, white_to_play)->tuple[Position,Position]:
        pass

    def _random_move(self, board:Board, color)->tuple[Position,Position]:
        moves = board.get_all_legal_moves(color)
        return random.choice(moves)
    
    @staticmethod
    def get_class_name(obj)->type:
        return type(obj)


class RandomStrategy(Strategy):
    def evaluate_board(self, board)->int:
        return 0  

    def best_move(self, board,depth,white_to_play)->tuple[Position,Position]:
        return self._random_move(board, 'white' if white_to_play else 'black')


class NormalStrategy(Strategy):
    def _get_piece_value(self, piece: Piece) -> int:
        piece_type = Strategy.get_class_name(piece)
        if piece_type == Pawn:
            return 150 
        elif piece_type == Knight:
            return 320 
        elif piece_type == Bishop:
            return 330 
        elif piece_type == Rook:
            return 500 
        elif piece_type == Queen:
            return 900 
        elif piece_type == King:
            return 20000 
        else:
            return 0    

    def evaluate_board(self, board:Board)->int:
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board.get_intersection(i, j).piece
                if piece is not None:
                    if piece.color == 'white':
                        score += self._get_piece_value(piece)
                    else:
                        score -= self._get_piece_value(piece)
        return score
    
    def best_move(self, board:Board, depth, white_to_play)->tuple[Position,Position]:
        best_score = -99999 if white_to_play else 99999
        best_move = self._random_move(board,'white' if white_to_play else 'black')
        random_number = random.randint(1, 5)
        if random_number == 1:
            return best_move
        
        legal_moves = board.get_all_legal_moves('white' if white_to_play else 'black')
        for move in legal_moves:
            copied_board = Board.copy_board(board)
            board.stack.push(copied_board)
            board.move(move[0],move[1])
            score, _ = self._minimax_pruning(board, depth - 1, -99999, 99999, not white_to_play)
            board.undo()
            if white_to_play and score > best_score:
                best_score = score
                best_move = move
            elif not white_to_play and score < best_score:
                best_score = score
                best_move = move
        return best_move
    
    def _minimax_pruning(self,board:Board, depth, alpha, beta, white_to_play)->tuple[int,tuple[Position,Position]]:
        if depth == 0 or board.is_game_over:
            return self.evaluate_board(board), None
        if white_to_play:
            best_score = -9999
            best_move = None
            legal_moves = board.get_all_legal_moves('white' if white_to_play else 'black')
            for move in legal_moves:
                copied_board = Board.copy_board(board)
                board.stack.push(copied_board)
                board.move(move[0],move[1])
                score, _ = self._minimax_pruning(board, depth - 1, alpha, beta, False)
                board.undo()
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move
        else:
            best_score = 9999
            best_move = None
            legal_moves = board.get_all_legal_moves('white' if white_to_play else 'black')
            for move in legal_moves:
                copied_board = Board.copy_board(board)
                board.stack.push(copied_board)
                board.move(move[0],move[1])
                score, _ = self._minimax_pruning(board, depth - 1, alpha, beta, True)
                board.undo()
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move


class BestStrategy(Strategy):
    def __init__(self) -> None:
        self.white_piece_values_with_position:dict = {
        Pawn: [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        Knight: [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ],
        Bishop: [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ],
        Rook: [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [0, 0, 0, 5, 5, 0, 0, 0]
        ],
        Queen: [
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
        ],
        King: [
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [20, 30, 10, 0, 0, 10, 30, 20]
        ]
    }
        
        self.black_piece_values_with_position = self._calculate_black_piece_values()

    def _calculate_black_piece_values(self)->dict:
        black_piece_values_with_position = {}

        for piece, values in self.white_piece_values_with_position.items():
            values_noir = [row[::-1] for row in values[::-1]]
            black_piece_values_with_position[piece] = values_noir

        return black_piece_values_with_position
    
    def _get_piece_value(self, piece: Piece, x: int, y: int, is_white: bool) -> int:
        piece_values_with_position = self.white_piece_values_with_position if is_white else self.black_piece_values_with_position
        piece_type = Strategy.get_class_name(piece)
        if piece_type == Pawn:
            return 150 + piece_values_with_position[piece_type][x][y]
        elif piece_type == Knight:
            return 320 + piece_values_with_position[piece_type][x][y]
        elif piece_type == Bishop:
            return 330 + piece_values_with_position[piece_type][x][y]
        elif piece_type == Rook:
            return 500 + piece_values_with_position[piece_type][x][y]
        elif piece_type == Queen:
            return 900 + piece_values_with_position[piece_type][x][y]
        elif piece_type == King:
            return 20000 + piece_values_with_position[piece_type][x][y]
        else:
            return 0

    def evaluate_board(self,board:Board) -> int:
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board.get_intersection(i, j).piece
                if piece is not None:
                    if piece.color == 'white':
                        score += self._get_piece_value(piece, i, j,True)
                    else:
                        score -= self._get_piece_value(piece, i, j,False)
        return score

    def best_move(self,board:Board,depth:int,white_to_play)->tuple[Position,Position]:
        best_score = -99999 if white_to_play else 99999
        best_move = self._random_move(board,'white' if white_to_play else 'black')
        legal_moves = board.get_all_legal_moves('white' if white_to_play else 'black')
        for move in legal_moves:
            copied_board = Board.copy_board(board)
            board.stack.push(copied_board)
            board.move(move[0],move[1])
            score, _ = self._minimax_pruning(board, depth - 1, -99999, 99999, not white_to_play)
            board.undo()
            if white_to_play and score > best_score:
                best_score = score
                best_move = move
            elif not white_to_play and score < best_score:
                best_score = score
                best_move = move
        return best_move
    

    def _minimax_pruning(self,board:Board, depth, alpha, beta, white_to_play)->tuple[int,tuple[Position,Position]]:
        if depth == 0 or board.is_game_over:
            return self.evaluate_board(board), None
        if white_to_play:
            best_score = -9999
            best_move = None
            legal_moves = board.get_all_legal_moves('white' if white_to_play else 'black')
            for move in legal_moves:
                copied_board = Board.copy_board(board)
                board.stack.push(copied_board)
                board.move(move[0],move[1])
                score, _ = self._minimax_pruning(board, depth - 1, alpha, beta, False)
                board.undo()
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move
        else:
            best_score = 9999
            best_move = None
            legal_moves = board.get_all_legal_moves('white' if white_to_play else 'black')
            for move in legal_moves:
                copied_board = Board.copy_board(board)
                board.stack.push(copied_board)
                board.move(move[0],move[1])
                score, _ = self._minimax_pruning(board, depth - 1, alpha, beta, True)
                board.undo()
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move

class AI:
    def __init__(self, depth: int, strategy: Strategy) -> None:
        self.depth:int = depth
        self.strategy:Strategy = strategy

    def evaluate_board(self, board)->int:
        return self.strategy.evaluate_board(board)

    def best_move(self, board, white_to_play)->tuple[Position,Position]:
        return self.strategy.best_move(board, self.depth, white_to_play)
