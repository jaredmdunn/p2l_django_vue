import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView

from .models import Game, GameScore, GameScoreParameters, Parameter


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['']

        return context


@login_required
def save_score(request, slug):
    user = request.user
    game = Game.objects.get(slug=slug)
    game_parameters = Parameter.objects.filter(game_id=game.pk)

    data = json.loads(request.body)

    score = data['score']
    param_data = json.loads(data['parameters'])
    # param_keys = param_data.keys()

    # game, parameters, and score are passed through data
    # depending on which game, parameters will be handled differently
    # score is saved
    # parameter values are saved

    if user.is_anonymous:
        msg = 'Sorry, you have to be logged in to save your score.'
    else:
        # if user has a previous score for that game and those parameter settings,
        # message should be `you beat your previous high score on this setting,
        # or "you can do better, you high score is ___"`
        prev_score_exists = True
        # loop through user's scores for specified game
        for user_score in GameScore.objects.filter(user=user, game=game):
            # loop through the parameters for the specific score
            for game_score_param in GameScoreParameters.objects.filter(gamescore=user_score, parameter_in=game_parameters):
                # if the values specified for the parameters do not match
                # what the user played in this game, a previous score does not exist
                if not (game_score_param.value == param_data[game_score_param.parameter.lower()]):
                    prev_score_exists = False
                    break
        
        if prev_score_exists:
            prev_score = GameScore.objects.get(user=user, game=game).order_by('-score')


        

        new_score = GameScore(user=user, game=game, score=score)

        

        msg = 'Your score was saved.'
    
    response = {
        'msg' : msg,
    }
    return JsonResponse(response)
