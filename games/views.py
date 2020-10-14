import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView

from .models import Game, GameScore, Parameter, ParameterValue


# class AnagramGameView(LoginRequiredMixin, TemplateView):
#     """View for the Anagram Hunt game"""
#     template_name = 'games/anagram-hunt.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = self.kwargs.get('slug')
#         game = Game.objects.get(slug=slug)
#         context['game'] = game
#         return context


class GameDetailView(LoginRequiredMixin, DetailView):
    """Detail view as a template to display different games; not used for Vue games"""
    model = Game

    def get_template_names(self):
        if self.object.type == self.object.GameType.VUE:
            return ['games/anagram-hunt.html']
        return super().get_template_names()


class ScoreListView(ListView):
    """List view to display scores on a leaderboard

    Used in urls of games and users as leaderboards and my-scores pages respectively, with
    my-scores being filtered to only show scores of the current user
    """
    model = Game
    template_name = 'games/score_list.html'

    def get_context_data(self, **kwargs) -> dict:
        """Adds context data to display the leaderboard

        Context:
            active_game: The game tab that is currently selected
            current_user: The logged-in user
            game_params: All of the game parameters for the active game
            params: The parameters by which to filter, set to defaults if not passed in
            tab_path: the url path to use on the game tabs, such it does not switch 
                between my-scores and leaderboards
            scores: a queryset of GameScore objects filtered and in descending order

        Returns:
            dict: A dictionary of context to be passed to the template
        """
        context = super().get_context_data(**kwargs)

        # set active game and current user
        slug = self.kwargs.get('slug')
        active_game = Game.objects.get(slug=slug) if slug else Game.objects.first()

        context['active_game'] = active_game
        context['current_user'] = self.request.user

        # set the game parameters
        game_params = active_game.parameters.all()
        context['game_params'] = game_params

        # set any blank parameter value to default
        params = self.request.GET.copy()
        for gp in game_params:
            if gp.slug not in params or not params[gp.slug]:
                params[gp.slug] = active_game.parameter_defaults[gp.slug]

        context['params'] = params

        scores = GameScore.objects.filter(game=active_game)

        # filter the scores (requires multiple filters because ManyToManyField)
        for param, value in params.items():
            scores = scores.filter(
                parameter_values__slug__iexact=value,
                parameter_values__parameter__slug=param
            )

        # initialize normal leaderboards tab_path
        context['tab_path'] = 'games:leaderboards'
        context['page_title'] = 'Leaderboards'

        # if on my-scores page, update tab_path and filter scores by user
        if '/account' in self.request.path_info:
            context['tab_path'] = 'users:my-scores'
            context['page_title'] = 'My Scores'
            context['user_stats'] = self.request.user.stats(active_game)
            scores = scores.filter(user=self.request.user)

        scores = scores.prefetch_related('user')

        context['scores'] = scores.order_by('-score')[:21]

        return context


@login_required
def save_score(request, slug: str):
    """Saves the score and returns a customized message based on whether a high score was achieved

    Args:
        request (HttpRequest): A request from the math facts saveScore function
        slug (str): The slug of the game

    Returns:
        JsonResponse: response containing the message to display to the user about score saving
    """
    # get data from the request
    user = request.user
    
    if user.is_anonymous:
        return JsonResponse({'msg': 'Sorry, you have to be logged in to save your score.'})

    game = Game.objects.get(slug=slug)

    data = json.loads(request.body)

    score = data['score']
    param_data = data['parameters']

    # game, parameters, and score are passed through data
    # depending on which game, parameters will be handled differently
    # score is saved
    # parameter values are saved
    # create new score

    new_score = GameScore(user=user, game=game, score=score)
    new_score.save()

    # add parameter values to the score
    for param_name, value in param_data.items():
        param = Parameter.objects.get(slug=param_name)
        param_value = param.values.get(value__iexact=value, parameter=param)
        new_score.parameter_values.add(param_value)

    # customize message based on whether a high score is achieved
    if new_score.is_high_score:
        msg = 'You beat the high score!'
    elif new_score.is_user_high_score:
        msg = 'You beat your high score!'
    else:
        msg = 'Your score was saved.'

    response = {
        'msg': msg,
    }
    return JsonResponse(response)
