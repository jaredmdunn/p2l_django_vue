from django.contrib import admin
from .models import Game, Parameter, ParameterValue, GameScore


class ParameterInline(admin.TabularInline):
    model = Parameter


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ['game']
    inlines = [ParameterInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return('slug',)
        return ()


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    model = GameScore
    list_display = ['user', 'game', 'score', 'created']


@admin.register(ParameterValue)
class ParameterValueAdmin(admin.ModelAdmin):
    model = ParameterValue
    list_display = ['value', 'parameter']
