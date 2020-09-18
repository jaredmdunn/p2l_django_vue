from django.contrib import admin
from .models import Game, Parameter, GameScore, GameScoreParameters

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ['game']

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    model = Parameter
    list_display = ['parameter','game_id']

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    model = GameScore
    list_display = ['user_id','game_id','score','created']

@admin.register(GameScoreParameters)
class GameScoreParametersAdmin(admin.ModelAdmin):
    model = GameScoreParameters
    list_display = ['gamescore_id','parameter_id','value']