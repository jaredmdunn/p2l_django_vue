import json

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from common.utils.text import unique_slug

class Game(models.Model):
    game = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)

    @property
    def parameter_defaults(self):
        param_value_dict = {}
        
        parameters = self.parameters

        for param in parameters.all():
            param_value_dict[param.slug] = param.default_value

        return param_value_dict

    def get_absolute_url(self):
        return reverse('games:game', args=[self.slug])
    
    def __str__(self): 
        return self.game

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['game']

class Parameter(models.Model):
    parameter = models.CharField(max_length=100)
    game = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='parameters'
    )
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)
    default_value = models.CharField(max_length=100)
    values = models.JSONField()

    def __str__(self): 
        return self.parameter

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

class GameScore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        related_name='game_scores'
    )
    game = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='game_scores'
    )
    score = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_high_score(self):
        game_score_params = self.game_score_params
        
        if GameScore.objects.filter(
            game_score_parameters__in=game_score_params, score__gt=self.score
        ).exists():
            return False
        
        return True

    @property
    def is_user_high_score(self):
        game_score_params = self.game_score_params

        if GameScore.objects.filter(
            game_score_parameters__in=game_score_params, score__gt=self.score, user=self.user
        ).exists():
            return False
        
        return True

    @property
    def game_score_params(self):
        params_values = self.game_score_parameters.all()

        param_value_query = Q()

        for pv in params_values:
            param_value_query = param_value_query | Q(
                parameter=pv.parameter, value=pv.value)

        return GameScoreParameters.objects.filter(param_value_query)

class GameScoreParameters(models.Model):
    gamescore = models.ForeignKey(
        'GameScore', on_delete=models.CASCADE, 
        related_name='game_score_parameters'
    )
    parameter = models.ForeignKey(
        'Parameter', on_delete=models.CASCADE, 
        related_name='game_score_parameters'
    )
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Game score parameters'