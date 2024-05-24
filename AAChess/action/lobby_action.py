from django.contrib.sessions.models import Session
from AAChess.models import User
from django.utils import timezone

class _LobbyAction:
    
    @staticmethod
    def online_users():
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        active_user_ids = [session.get_decoded().get('_auth_user_id', None) for session in active_sessions]
        active_user_ids = list(set(filter(None, active_user_ids)))
        active_users = User.objects.filter(id__in=active_user_ids)
        active_users_data = [(user.username, user.id) for user in active_users]
        return active_users_data

