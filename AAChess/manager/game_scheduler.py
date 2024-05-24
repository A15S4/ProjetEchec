"""
Nom du fichier : game_scheduler.py
Contexte : Ce fichier contient la classe permettant de gérer les actions effectué en parallèle par le GameManager.
Auteurs : Alexandre Chapleau
"""
from .game_manager import GameManager
import threading


class GameScheduler:
    def __init__(self):
        self.game_manager = GameManager.get_instance()
        self.start_timer()

    def start_timer(self):   
        self.timer = threading.Timer(1, self.scheduled_actions)
        self.timer.start()

    def scheduled_actions(self):
        if len(self.game_manager.games) > 0:
            for game in self.game_manager.games:
                if game.game_type == 'PVA':
                    ai = game.get_player('AI')
                    if ai.player_turn:
                        self.game_manager.manage_ai(game,ai)
                else:
                    self.game_manager.reduce_players_time(game)
                self.game_manager.check_for_winner(game) 
        self.start_timer()


    
    
