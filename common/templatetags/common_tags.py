from games.models import Game
from django import template

register = template.Library()

@register.inclusion_tag('common/game_links.html')
def show_game_links():
    games = Game.objects.all()
    return {'games': games}

@register.inclusion_tag('common/game_scores.html')
def show_game_scores(game):
    game_params = game.parameters
    return {'game_params': game_params}
