from games.models import Game
from django import template

register = template.Library()

@register.inclusion_tag('common/game_links.html')
def show_game_links():
    games = Game.objects.all()
    return {'games': games}