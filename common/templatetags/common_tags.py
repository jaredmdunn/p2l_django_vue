from games.models import Game
from users.models import Review
from django import template

register = template.Library()


@register.inclusion_tag('common/game_boxes.html')
def show_game_boxes():
    games = Game.objects.all()
    return {'games': games}


@register.inclusion_tag('common/game_links.html')
def show_game_links():
    games = Game.objects.all()
    return {'games': games}


@register.inclusion_tag('common/game_scores.html')
def show_game_scores(game):
    game_params = game.parameters
    return {'game_params': game_params}


@register.inclusion_tag('common/featured_reviews.html')
def show_featured_reviews(user):
    featured_reviews = Review.objects.filter(featured=True).order_by('created')
    return {'featured_reviews': featured_reviews, 'user': user}
