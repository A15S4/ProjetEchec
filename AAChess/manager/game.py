import time
from ..Chess.Board import Board
from .game_user import Player
from .ai import *
import copy


class Game:
    def __init__(self, player1: Player, player2: Player, game_type: str,ai_difficulty:Strategy=None)->None:
        self.__player1:Player = player1
        self.__player2:Player = player2
        self.__board:Board = Board()
        self.__winner:str|None = None
        self.__game_type:str = game_type
        self.__start:time = time.perf_counter()
        self.__ai:AI = AI(depth=2,strategy=ai_difficulty) if game_type == 'PVA' else None

    
    @property
    def player1(self)->Player:
        return self.__player1

    @property
    def player2(self)->Player:
        return self.__player2
    
    @property
    def board(self)->Board:
        return self.__board

    @property
    def winner(self)->str|None:
        return self.__winner
    
    @winner.setter
    def winner(self,value):
        self.__winner = value

    @property
    def start(self)->float:
        return self.__start
    
    @property
    def game_type(self)->str:
        return self.__game_type
    
    @property
    def ai(self)->AI|None:
        return self.__ai
    
    def to_dict(self)->dict:
        return {
            'player1': self.__player1.to_dict(),
            'player2': self.__player2.to_dict(),
            'game_type': self.__game_type,
            'board': self.__board.board_json(),  
            'start_time': self.__start,
            'winner': self.__winner
        }
    
    def get_player(self,username)->Player:
        if self.__player1.username == username:
            return self.__player1
        elif self.__player2.username == username:
            return self.__player2
        else:
            return None
        
    def get_opponent_color(self,color)->str:
        return 'white' if color=='black' else 'black'
    
    def change_turn(self)->None:
        self.__player1.player_turn = not self.__player1.player_turn
        self.__player2.player_turn = not self.__player2.player_turn
     

    def reduce_time(self,player1:Player,player2:Player)->None:
        player = player1 if player1.player_turn else player2
        player.time_left = max(0, player.time_left - 1)
        if player.time_left == 0:
            self.winner = player1.username if player == player2 else player2.username

    def move_ai(self)->tuple[Position,Position]:
        board = copy.deepcopy(self.__board)
        ai_player = self.get_player('AI')
        return self.ai.best_move(board,True if ai_player.color == 'white' else False)

    
        