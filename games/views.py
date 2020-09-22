import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView

from .models import Game, GameScore, GameScoreParameters, Parameter


class GameDetailView(DetailView):
    model = Game

@login_required
def save_score(request, slug):
    user = request.user
    game = Game.objects.get(slug=slug)

    data = json.loads(request.body)

    score = data['score']
    param_data = data['parameters']

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

        new_score = GameScore(user_id=user, game_id=game, score=score)
        new_score.save()
        
        for key, value in param_data.items():
            param = Parameter.objects.get(slug=key)
            new_score_param = GameScoreParameters(gamescore_id=new_score, parameter_id=param, value=value)
            new_score_param.save()

        if new_score.is_high_score:
            msg = 'You beat the high score!'
        elif new_score.is_user_high_score:
            msg = 'You beat your high score!'
        else:
            msg = 'Your score was saved.'
    
    response = {
        'msg' : msg,
    }
    return JsonResponse(response)
