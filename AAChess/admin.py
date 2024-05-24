from django.contrib import admin
from .models import User,Stats,TotalPiecesPlayed,AuthToken

#affiche les tables de la db suivantes dans le module admin de Django 
admin.site.register(User)
admin.site.register(Stats)
admin.site.register(TotalPiecesPlayed)
admin.site.register(AuthToken)