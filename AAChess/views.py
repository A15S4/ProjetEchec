"""
Nom du fichier : views.py
Contexte : Ce fichier contient les vues de l'application Django pour gérer les différentes fonctionnalités de l'application, telles que l'authentification des utilisateurs, la gestion des parties de jeu, et la présentation des statistiques.
Auteurs : Alexandre Chapleau, Aissa Bouaraguia
"""

from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render,redirect
from .action.lobby_action import _LobbyAction
from .action.stats_action import StatsAction
from .action.chall_action import ChallAction
from .DAO.user_dao import UserDao
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .forms import SignUpForm,LoginForm
from .manager.game_manager import GameManager
from .manager.game_scheduler import GameScheduler
from .Chess.Position import Position
import random


game_manager = GameManager.get_instance()
fonctions_periodiques = GameScheduler()

def index(request):
    success_message = request.session.pop('success_message', None)
    theme= request.session.get('theme', 'classic')
    context = {
            'form':LoginForm(request.POST or None),
            "theme": theme
    }
    if success_message:
        context['success_message'] = success_message
    if request.method == 'POST':
        if context['form'].is_valid():
            username = context['form'].cleaned_data.get('username')
            password = context['form'].cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                key = UserDao.generate_auth_token(user)
                UserDao.del_auth_token(user)
                UserDao.save_auth_token(user,key)
                request.session['key'] = key
                return HttpResponseRedirect('/lobby/')  
            else:  
                context['message']="Les informations d'identification sont incorrectes."
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
    
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserDao.create_user_stats(user)
            UserDao.create_user_total_pieces_played(user)
            messages.success(request, 'Usager ajouté avec succès!')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form})

@login_required
def lobby(request):
    theme= request.session.get('theme', 'classic')
    if request.method == 'POST':
        value = request.POST.get("type")
        actions = {
            "play": "/game/",
            "stats": "/stats/",
            "chall": "/chall/",
            "rules": "/rules/",
            "logout": "/logout/"
        }
        return redirect(actions[value])
    active_users = _LobbyAction.online_users()
    context = {
            'active_users': len(active_users),
            "theme" : theme
        }

    template = loader.get_template('lobby.html')
    return HttpResponse(template.render(context, request))                       

@login_required
def stats(request):
    theme= request.session.get('theme', 'classic')
    key = request.session['key']
    stats_data = UserDao.get_stats(key)
    pieces_data = UserDao.get_total_pieces_played(key)
    name = stats_data.player.username
    winrate = StatsAction.calculate_win_percentage(stats_data)
    total_time = StatsAction.format_game_time(stats_data.game_time_total)
    pieces_percentage = StatsAction.calculate_piece_percentages(pieces_data)

    context = {
        'winrate': winrate,
        'name': name,
        'total_time': total_time,
        'pieces_percentage': pieces_percentage,
        'theme': theme
    }

    template = loader.get_template('stats.html')
    return HttpResponse(template.render(context, request))

@login_required
def game(request):
    theme= request.session.get('theme', 'classic')
    token = request.session['key']
    username = UserDao.get_username_from_token(token)
    game_manager.request_game(token)
    template = loader.get_template('game.html')
    return HttpResponse(template.render({'username':username, 'theme':theme}, request))

@login_required
def training(request): 
    theme= request.session.get('theme', 'classic')
    token = request.session['key']
    pieces_color = None
    difficulty = None

    if request.method == 'POST':
        pieces_color = request.POST.get("couleur_piece")
        difficulty = request.POST.get("difficulte")
    username = UserDao.get_username_from_token(token)
    game_manager.start_training(token,pieces_color,difficulty)
    context = {
        'couleur_piece': pieces_color,
        'difficulte': difficulty,
        'username':username,
        'theme':theme
    }
    template = loader.get_template('game.html')
    return HttpResponse(template.render(context, request))

@login_required
def chall(request):
    theme= request.session.get('theme', 'classic')
    all_lines = ChallAction.read_csv('games.csv')
    game_number = random.randint(1, 5)
    game_moves = ChallAction.filter_game_moves(all_lines, game_number)
    movement_pair = ChallAction.get_elements(game_moves)

    if not movement_pair:
        return HttpResponse("No movements found for the selected game number.")

    game_state_1 = ChallAction.parse_movement(movement_pair[0])
    game_state_2 = ChallAction.parse_movement(movement_pair[1])

    context = {
        "game_state_1": game_state_1[0],
        "turn_1": game_state_1[1],
        "game_state_2": game_state_2[0],
        "turn_2": game_state_2[1],
        "theme" : theme
    }

    template = loader.get_template('chall.html')
    return HttpResponse(template.render(context, request))

@login_required
def rules(request):
    template = loader.get_template('rules.html')
    return HttpResponse(template.render({}, request))


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def remove_from_list(request):
    if request.method == 'POST':
        token = request.session.get('key')  
        if token:
            game_manager.remove_from_lists(token)
            return JsonResponse({'success': True})  
        else:
            return JsonResponse({'success': False, 'error': 'Token not found'}, status=400)  
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)  

@login_required
def game_data(request):
    if request.method == 'GET':
        token = request.session['key']
        data=game_manager.get_data(token)
        response_data = {'data': data}
        return JsonResponse(response_data)
    else:
        error_message = {'error': 'Méthode HTTP non autorisée'}
        return JsonResponse(error_message, status=405)

@login_required   
def action(request):
    if request.method == 'POST':
        token = request.session['key']
        data = json.loads(request.body)
        start_position = data['start']
        end_position = data['end']
        start = Position(row= start_position[0], column=start_position[1])
        end = Position(row=end_position[0], column=end_position[1])
        action = game_manager.game_action(start,end,token)
        return JsonResponse({'data':action})
    else:
        error_message = {'error': 'Méthode HTTP non autorisée'}
        return JsonResponse(error_message, status=405)               