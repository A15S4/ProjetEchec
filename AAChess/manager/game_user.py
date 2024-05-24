from ..Chess.Piece import Piece

class Player:
    def __init__(self,username:str,color:str,time_left:int): 
        self.__username:str = username
        self.__color:str = color
        self.__player_turn:bool = self.__color == 'white'
        self.__time_left:int = time_left
        self.__piece_played:dict ={'king':0,'queen':0,'bishop':0,'rook':0,'pawn':0,'knight':0}
    
    @property
    def username(self)->str:
        return self.__username
    
    @username.setter
    def username(self,value):
        self.__username = value
    
    @property
    def color(self)->str:
        return self.__color
   
    @property
    def time_left(self)->int:
        return self.__time_left
    
    @time_left.setter
    def time_left(self,value):
        self.__time_left = value
    
    @property
    def player_turn(self)->bool:
        return self.__player_turn
    
    @player_turn.setter
    def player_turn(self,value):
        self.__player_turn = value

    @property
    def piece_played(self)->dict:
        return self.__piece_played
    
    @piece_played.setter
    def piece_played(self, piece_first_letter:str)->None:
        self.__piece_played[piece_first_letter] += 1

    def to_dict(self)->dict:
        return {
            'username': self.__username,
            'player_turn': self.__player_turn,
            'color': self.__color,
            'time_left': self.__time_left,
            'piece_played': self.__piece_played,
        }

    def update_pieces_played(self,piece:Piece)->None:
        self.__piece_played[piece.name] += 1
    
        
    