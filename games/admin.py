from django.contrib import admin
from .models import Game, Parameter, GameScore, GameScoreParameters

class ParameterInline(admin.TabularInline):
    model = Parameter
    list_display = ['parameter','slug','game_id', 'values']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ['game']
    inlines = [ParameterInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return('slug',)
        return ()


class GameScoreParametersInline(admin.TabularInline):
    model = GameScoreParameters
    list_display = ['gamescore_id','parameter_id','value']


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    model = GameScore
    list_display = ['user_id','game_id','score','created']
    inlines = [GameScoreParametersInline]