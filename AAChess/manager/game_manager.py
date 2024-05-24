"""
Nom du fichier : game_manager.py
Contexte : Ce fichier contient la classe permettant de gérer les instances de toutes les parties.
Auteurs : Alexandre Chapleau
"""

from ..DAO.user_dao import UserDao
import random
from .game import Game
from .game_user import Player
import time
from ..Chess.Position import Position
from ..Chess.Board import Board
from .ai import *

class GameManager:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs) 
            cls._instance._waiting_players_pvp = []
            cls._instance._games = []

        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()
    
    @property
    def waiting_players_pvp(self)->list[str]:
        return self._waiting_players_pvp
    
    @property
    def games(self)->list[Game]:
        return self._games
    
    def request_game(self, token)->None:
        user = UserDao.get_username_from_token(token)
        
        if user not in self.waiting_players_pvp:
            self.waiting_players_pvp.append(user)

        if len(self.waiting_players_pvp) >= 2:
            player1 = self.waiting_players_pvp.pop(0)
            player2 = self.waiting_players_pvp.pop(0)
            self.start_game(player1, player2)

    def start_game(self, user1,user2)->None:
        users = [user1, user2]
        random.shuffle(users)
        player1 = Player(users[0],'white',600)
        player2 = Player(users[1],'black',600)

        game = Game(player1, player2, 'PVP')
        self.games.append(game)

    def start_training(self,token,piece_color,difficulty)->None:
        player = UserDao.get_username_from_token(token)
        if self.get_game(player) is None:
            difficulties = {
                'Facile': RandomStrategy,
                'Normal': NormalStrategy,
                'Difficile': BestStrategy
            }

            colors = {
                'Blanc': 'white',
                'Noir': 'black'
            }

            opponent_difficulty = difficulties.get(difficulty, RandomStrategy)()
            color = colors.get(piece_color, 'white')
            opponent_color = 'black' if color == 'white' else 'white'

            player1 = Player(player,color,999)
            player2 = Player('AI',opponent_color,999)
            game = Game(player1, player2, 'PVA', opponent_difficulty)
            self.games.append(game)

    def get_game(self, username)->Game|None:
        for game in self.games:
            if game.player1.username == username or game.player2.username == username:
                return game
        return None
    
    def reduce_players_time(self,game:Game)->None:
        game.reduce_time(game.player1,game.player2)

    def check_for_winner(self,game:Game)->None:
        if game.winner != None:
            self.end_game(game)

    def update_player_stats(self,game)->None:
        for player in [game.player1, game.player2]:
            if player.username != 'AI':
                UserDao.update_total_pieces_played(player.username, player.piece_played)
                game_result = 'WON' if game.winner == player.username else 'LOST'
                UserDao.update_stats(username=player.username, last_game=game_result, total_win=int(game.winner == player.username), 
                                     total_loss=int(game.winner != player.username), game_time_total=int(time.perf_counter() - game.start))
                
    def update_game_winner_stats(self, game)->None:
        if game.winner:
            if game.board.draw:
                for player in [game.player1, game.player2]:
                    if player.username != 'AI':
                        UserDao.update_stats(username=player.username, last_game='DRAW', total_draw=1, game_time_total=int(time.perf_counter() - game.start))
            else:
                winner = game.player1 if game.winner == game.player1.username else game.player2
                loser = game.player2 if game.winner == game.player1.username else game.player1
                if winner.username != 'AI':
                    UserDao.update_stats(username=winner.username, last_game='WON', total_win=1, game_time_total=int(time.perf_counter() - game.start))
                if loser.username != 'AI':
                    UserDao.update_stats(username=loser.username, last_game='LOST', total_loss=1, game_time_total=int(time.perf_counter() - game.start))
                

    def end_game(self, game: Game)->None:
        self.update_player_stats(game)
        self.update_game_winner_stats(game)
        time.sleep(1)
        self.games.remove(game)

    def remove_from_lists(self,token)->None:
        username = UserDao.get_username_from_token(token)
        if username:
            if username in self._waiting_players_pvp:
                self._waiting_players_pvp.remove(username)
            game:Game = self.get_game(username)
            if game:
                if game.player1.username == username:
                    game.winner = game.player2.username
                else:
                    game.winner = game.player1.username

    def get_data(self,token)->dict|str:
        username = UserDao.get_username_from_token(token)
        game = self.get_game(username)
        if game:
            return game.to_dict()
        elif username in self._waiting_players_pvp:
            return "WAITING"
        else:
            return UserDao.last_game(username)
        
    def game_action(self,start:Position,end:Position,token)->bool:
        username = UserDao.get_username_from_token(token)
        game:Game = self.get_game(username)
        player:Player = game.get_player(username)
        temp_board = Board.copy_board(game.board)
        piece = game.board.get_intersection(start.row,start.column).piece
        opponent_color = game.get_opponent_color(player.color)
        if player.player_turn:
            if game.board.pre_move(start,end):
                player.update_pieces_played(piece)
                if game.board.is_checkmate(opponent_color):
                    game.winner = username
                game.change_turn()
                game.board.last_move = (start,end)
                game.board.stack.push(temp_board)
                return True
        return False
    
    def manage_ai(self,game:Game,ai:Player)->None:
        if game.winner == None:
            move = game.move_ai()
            temp_board = Board.copy_board(game.board)
            opponent_color = game.get_opponent_color(ai.color)
            start,end = move
            game.board.move(start,end)
            if game.board.is_checkmate(opponent_color):
                game.winner = 'AI'
            game.board.stack.push(temp_board)
            game.change_turn()