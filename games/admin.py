from django.contrib import admin
from .models import Game, Parameter, GameScore, GameScoreParameters

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ['game']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return('slug',)
        return ()

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    model = Parameter
    list_display = ['parameter','slug','game_id', 'values']

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    model = GameScore
    list_display = ['user_id','game_id','score','created']

@admin.register(GameScoreParameters)
class GameScoreParametersAdmin(admin.ModelAdmin):
    model = GameScoreParameters
    list_display = ['gamescore_id','parameter_id','value']