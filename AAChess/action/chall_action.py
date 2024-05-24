"""
Nom du fichier : chall_action.py
Contexte : Ce fichier contient la classe permettant de gérer les données d'un fichier CSV.
Auteurs : Alexandre Chapleau
"""
import csv
import random
from django.contrib.staticfiles import finders


class ChallAction:
    @staticmethod
    def read_csv(file_name):
        file_path = finders.find(file_name)
        if not file_path:
            return []
    
        with open(file_path) as file:
            csv_reader = csv.reader(file)
            return list(csv_reader)
        
    @staticmethod
    def filter_game_moves(all_lines, game_number):
        return [row for row in all_lines if row[0] == str(game_number)]

    @staticmethod
    def get_elements(lst):
        if not lst:
            return ()
        
        three_quarters_point = len(lst) // random.randint(2, 5)
        if three_quarters_point < len(lst) - 1:
            return (lst[three_quarters_point][2], lst[three_quarters_point + 1][2])
        else:
            return ()
        
    @staticmethod
    def parse_movement(movement):
        clean_movement = movement.replace("(", "").replace(")", "")
        return clean_movement.split(" ")