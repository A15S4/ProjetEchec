from ..models import User, Stats, TotalPiecesPlayed, AuthToken
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from typing import Optional



class UserDao:
    """
    Classe contenant des méthodes utilitaires pour la gestion des utilisateurs.
    """

    @staticmethod
    def create_user_stats(user: User) -> None:
        """
        Crée une instance de Stats pour l'utilisateur donné.

        Args:
            user (User): L'utilisateur pour lequel créer les statistiques.
        """
        Stats.objects.create(player=user)
        
    @staticmethod
    def create_user_total_pieces_played(user: User) -> None:
        """
        Crée une instance de TotalPiecesPlayed pour l'utilisateur donné.

        Args:
            user (User): L'utilisateur pour lequel créer le total des pièces jouées.
        """
        TotalPiecesPlayed.objects.create(player=user)

    @staticmethod
    def generate_auth_token(user: User) -> str:
        """
        Génère un token d'authentification pour l'utilisateur donné.

        Args:
            user (User): L'utilisateur pour lequel générer le token.

        Returns:
            str: Le token d'authentification généré.
        """
        return default_token_generator.make_token(user)

    @staticmethod
    def save_auth_token(user: User, token: str) -> None:
        """
        Enregistre le token d'authentification pour l'utilisateur donné.

        Args:
            user (User): L'utilisateur pour lequel enregistrer le token.
            token (str): Le token d'authentification à enregistrer.
        """
        AuthToken.objects.create(user=user, token=token)

    @staticmethod
    def del_auth_token(user):
        try:
            token = AuthToken.objects.get(user=user)
            token.delete()
        except AuthToken.DoesNotExist:
            pass

    @staticmethod
    def get_username_from_token(token: str) ->str:
        """
        Récupère le nom d'utilisateur associé à un token d'authentification.

        Args:
            token (str): Le token d'authentification pour lequel récupérer le nom d'utilisateur.

        Returns:
            str: Le nom d'utilisateur associé au token donné.

        Raises:
            ValueError: Si aucun utilisateur n'est trouvé pour le token donné.
        """
        try:
            auth_token = AuthToken.objects.get(token=token)
            return auth_token.user.username
        except AuthToken.DoesNotExist:
            raise ValueError("Mauvais token")

    @staticmethod
    @receiver(user_logged_out)
    def delete_auth_token(sender, **kwargs) -> None:
        """
        Supprime le token d'authentification de l'utilisateur lorsqu'il se déconnecte.

        Args:
            sender: L'expéditeur du signal.
            **kwargs: Arguments supplémentaires passés avec le signal.
        """
        user = kwargs['user']
        try:
            token = AuthToken.objects.get(user=user)
            token.delete()
        except AuthToken.DoesNotExist:
            pass

    @staticmethod
    def update_stats(username: str, game_time_total: Optional[int] = None, last_game:Optional[str] = None, total_win: Optional[int] = None, total_draw: Optional[int] = None, total_loss: Optional[int] = None, total_puzzles: Optional[int] = None) -> bool:
        """
        Met à jour les statistiques de l'utilisateur avec les valeurs fournies.

        Args:
            username (str): Le nom d'utilisateur de l'utilisateur à mettre à jour.
            game_time_total (int, optional): Temps de jeu total à ajouter.
            total_win (int, optional): Nombre total de victoires à ajouter.
            total_draw (int, optional): Nombre total de matchs nuls à ajouter.
            total_loss (int, optional): Nombre total de défaites à ajouter.
            total_puzzles (int, optional): Nombre total de puzzles à ajouter.

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        try:
            user = User.objects.get(username=username)
            stats = Stats.objects.get(player=user)
            if game_time_total is not None:
                stats.game_time_total += game_time_total
            if last_game is not None:
                stats.last_game = last_game
            if total_win is not None:
                stats.total_win += total_win
            if total_draw is not None:
                stats.total_draw += total_draw
            if total_loss is not None:
                stats.total_loss += total_loss
            if total_puzzles is not None:
                stats.total_puzzles += total_puzzles
            stats.save()
            return True
        except (User.DoesNotExist, Stats.DoesNotExist):
            return False
        
    @staticmethod
    def update_total_pieces_played(username: str, pieces_played: dict[str, int]) -> bool:
        """
        Met à jour le total des pièces jouées par l'utilisateur avec les valeurs fournies.

        Args:
            username (str): Le nom d'utilisateur de l'utilisateur à mettre à jour.
            pieces_played (Dict[str, int]): Un dictionnaire contenant le nombre de pièces jouées de chaque type.

        Returns:
            bool: True si la mise à jour a réussi, False sinon.
        """
        try:
            user = User.objects.get(username=username)
            total_pieces_played = TotalPiecesPlayed.objects.get(player=user)
            for piece, count in pieces_played.items():
                if hasattr(total_pieces_played, piece):
                    setattr(total_pieces_played, piece, getattr(total_pieces_played, piece) + count)
            total_pieces_played.save()
            return True
        except (User.DoesNotExist, TotalPiecesPlayed.DoesNotExist):
            return False
        
    @staticmethod 
    def last_game(username:str)->str:
        user = User.objects.get(username=username)
        stats = Stats.objects.get(player=user)
        return stats.last_game
    
    @staticmethod
    def get_stats(token:str)->str:
        username = UserDao.get_username_from_token(token)
        user = User.objects.get(username=username)
        return Stats.objects.get(player=user)
    
    @staticmethod
    def get_total_pieces_played(token:str)->str:
        username = UserDao.get_username_from_token(token)
        user = User.objects.get(username=username)
        return TotalPiecesPlayed.objects.get(player=user)