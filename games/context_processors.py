from users.models import Review
from .models import Game

def add_to_context(request):
    """Add games and  featured reviews to context for use in templates."""
    return {
        'all_games': Game.objects.all(),
        'featured_reviews': Review.objects.filter(featured=True).order_by('created')
    }