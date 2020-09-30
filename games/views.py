import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView, ListView

from .models import Game, GameScore, Parameter, ParameterValue


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game


class ScoreListView(ListView):
    model = Game
    template_name = 'games/score_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        active_game = Game.objects.prefetch_related(
            'parameters').get(slug=self.kwargs['slug'])
        context['active_game'] = active_game
        context['current_user'] = self.request.user

        game_params = active_game.parameters
        context['game_params'] = game_params.all()

        params = self.request.GET.copy()

        # sets any blank parameter value to default
        for gp in game_params.all():
            if gp.slug not in params or not params[gp.slug]:
                params[gp.slug] = active_game.parameter_defaults[gp.slug]

        context['params'] = params

        scores = GameScore.objects.filter(game=active_game)

        # filters the scores (requires multiple filters because ManyToManyField)
        for param, value in params.items():
            scores = scores.filter(
                parameter_values__value__iexact=value,
                parameter_values__parameter__slug=param
            )

        scores = scores.prefetch_related('user')

        context['scores'] = scores.order_by('-score')[:21]

        return context

    # def get_queryset(self):
    #     qs = GameScore.objects.all()
    #     if '/my-scores' in self.request.path_info:
    #         qs = qs.filter(user=self.request.user)
    #     return qs.prefetch_related('game', 'parameter')


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

        new_score = GameScore(user=user, game=game, score=score)
        new_score.save()

        for key, value in param_data.items():
            param = Parameter.objects.get(slug=key)
            param_value = param.values.get(value__iexact=value)
            new_score.parameter_values.add(param_value)

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


# class ScoreListView(ListView):
#     model = Game
#     template_name = 'games/score_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # order_fields, order_key, direction = self.get_order_settings()

#         context['active_game'] = Game.objects.get(slug=self.kwargs['slug'])
#         context['current_user'] = self.request.user

#         return context

#     def get_queryset(self):
#     #     ordering = self.get_ordering()
#         qs = GameScore.objects.all()

#     #     if '/my-scores' in self.request.path_info:
#     #         qs = qs.filter(user=self.request.user)

#         return qs
