from games.models import Game
from users.models import CustomUser, Review
from django import template

register = template.Library()


@register.inclusion_tag('common/game_boxes.html')
def show_game_boxes():
    """Displays a series of boxes for each game.
    Each box shows the title of the game, a game description, and has
    links to the game leaderboards, and the game itself
    """
    games = Game.objects.all()
    return {'games': games}


@register.inclusion_tag('common/game_links.html')
def show_game_links():
    """Displays a series of links to each game."""
    games = Game.objects.all()
    return {'games': games}


# @register.inclusion_tag('common/leaderboard_link.html')
# def show_leaderboard_link(page):
#     """Displays a link to the leaderboards or my scores page for first game in the database.
#     Takes a page name: 'leaderboards' or 'my-scores' to indicate which link to display
#     """
#     games = Game.objects.all()
#     first_game_slug = games.first().slug
#     return {'first_game_slug': first_game_slug, 'page': page}


@register.inclusion_tag('common/featured_reviews.html')
def show_featured_reviews(user):
    """Displays a carousel of all the featured reviews"""
    featured_reviews = Review.objects.filter(featured=True).order_by('created')
    return {'featured_reviews': featured_reviews, 'user': user}


# @register.inclusion_tag('common/show_stats.html')
# def show_stats(user, game):
#     """Displays a users stats for a specific game"""
#     stats = user.stats(game)
#     return {'stats': stats}
