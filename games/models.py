import json

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from common.utils.text import unique_slug

class Game(models.Model):
    game = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)

    def get_absolute_url(self):
        return reverse('games:game', args=[self.slug])
    
    def __str__(self): 
        return self.game

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

class Parameter(models.Model):
    INPUT_TYPES = (
        ('select', 'select'),
        ('number', 'number'),
    )
    parameter = models.CharField(max_length=100)
    game_id = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='parameters'
    )
    slug = models.SlugField(max_length=50, unique=True, null=False, editable=False)
    input_type = models.CharField(max_length=50, choices=INPUT_TYPES)
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
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
        related_name='game_scores'
    )
    game_id = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='game_scores'
    )
    score = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_high_score(self):
        params_values = self.game_score_parameters.all()

        params_values_dict = {}
        for pv in params_values:
            params_values_dict[pv.parameter_id] = pv.value

        param_value_query = Q()
        for key, value in params_values_dict.items():
            param_value_query = param_value_query | Q(parameter_id=key, value=value)

        game_score_params = GameScoreParameters.objects.filter(param_value_query)
        
        if GameScore.objects.filter(
            game_score_parameters__in=game_score_params, score__gt=self.score).exists():
            return False
        else:
            return True

    @property
    def is_user_high_score(self):
        params_values = self.game_score_parameters.all()

        params_values_dict = {}
        for pv in params_values:
            params_values_dict[pv.parameter_id] = pv.value

        param_value_query = Q()
        for key, value in params_values_dict.items():
            param_value_query = param_value_query | Q(parameter_id=key, value=value)

        game_score_params = GameScoreParameters.objects.filter(param_value_query)

        if GameScore.objects.filter(
            game_score_parameters__in=game_score_params, 
            score__gt=self.score, user_id=self.user_id).exists():
            return False
        else:
            return True

class GameScoreParameters(models.Model):
    gamescore_id = models.ForeignKey(
        'GameScore', on_delete=models.CASCADE, 
        related_name='game_score_parameters'
    )
    parameter_id = models.ForeignKey(
        'Parameter', on_delete=models.CASCADE, 
        related_name='game_score_parameters'
    )
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Game score parameters'