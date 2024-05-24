"""
Nom du fichier : models.py
Contexte : Dans Django, les classes sont des tables dans une base de données relationnelle.
Auteurs : Alexandre Chapleau
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modèle représentant un utilisateur.
    """
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)

class Stats(models.Model):
    """
    Modèle représentant les statistiques d'un joueur.
    """
    id = models.AutoField(primary_key=True)
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    game_time_total = models.IntegerField(default=0)
    last_game = models.CharField(max_length=10, default='null')
    total_win = models.IntegerField(default=0)
    total_draw = models.IntegerField(default=0)
    total_loss = models.IntegerField(default=0)
    total_puzzles = models.IntegerField(default=0)

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet. Utile pour le module admin de Django
        """
        return f"{self.player.username}"

class TotalPiecesPlayed(models.Model):
    """
    Modèle représentant le total des pièces jouées par un joueur.
    """
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    king = models.IntegerField(default=0)
    queen = models.IntegerField(default=0)
    rook = models.IntegerField(default=0)
    pawn = models.IntegerField(default=0)
    knight = models.IntegerField(default=0)
    bishop = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet. Utile pour le module admin de Django
        """
        return f"{self.player.username}"

    
    def save(self, *args, **kwargs):
        """
        Met à jour le total des pièces jouées avant de sauvegarder l'objet.
        équivalent en SQlite
        CREATE TRIGGER IF NOT EXISTS update_total_pieces_played_trigger
        AFTER INSERT ON total_pieces_played
        BEGIN
            UPDATE total_pieces_played
            SET total = NEW.king + NEW.queen + NEW.rook + NEW.pawn + NEW.knight + NEW.bishop;
        END;
        """
        self.total = self.king + self.queen + self.rook + self.pawn + self.knight + self.bishop
        super(TotalPiecesPlayed, self).save(*args, **kwargs)



class AuthToken(models.Model):
    """
    Modèle représentant un token d'authentification pour un utilisateur.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet. Utile pour le module admin de Django
        """
        return f"{self.user.username}"