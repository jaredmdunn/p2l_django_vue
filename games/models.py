from django.conf import settings
from django.db import models

class Game(models.Model):
    game = models.CharField(max_length=100)

    def __str__(self): 
        return self.game

class Parameter(models.Model):
    parameter = models.CharField(max_length=100)
    game_id = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='parameters'
    )

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