"""
Nom du fichier : urls.py
Contexte : Ce fichier définit les URL mappées aux vues de l'application Django, gérant la navigation et les requêtes des utilisateurs.
Auteurs : Alexandre Chapleau
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('lobby/',views.lobby,name='lobby'),
    path('logout/',views.logout_view,name='logout'),
    path('remove_from_list/',views.remove_from_list,name='remove_from_list'),
    path('stats/',views.stats,name='stats'),
    path('chall/',views.chall,name='chall'),
    path('rules/',views.rules,name='rules'),
    path('game_data/',views.game_data),
    path('game/',views.game,name='game'),
    path('action/',views.action,name='action'),
    path('training/',views.training,name='training'),
]