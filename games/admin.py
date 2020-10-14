from django.contrib import admin

from .models import Game, Parameter, ParameterValue, GameScore


class ParameterInline(admin.TabularInline):
    """Tabular inline for the Parameter model"""
    model = Parameter
    autocomplete_fields = ['default_value']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game admin displaying the game and parameter inline"""
    model = Game
    list_display = ['game', 'type']
    inlines = [ParameterInline]

    def get_readonly_fields(self, request, obj=None) -> tuple:
        """Adds slug as a readonly field to change form."""
        if obj:
            return('slug',)
        return ()


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    """GameScore admin displaying user, game, score, and created"""
    model = GameScore
    autocomplete_fields = ['user']
    list_display = ['user', 'game', 'score', 'created']


@admin.register(ParameterValue)
class ParameterValueAdmin(admin.ModelAdmin):
    """ParameterValue admin displaying value and parameter"""
    model = ParameterValue
    list_display = ['value', 'parameter']
    search_fields = ['value']
