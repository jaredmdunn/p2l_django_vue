import json

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from common.utils.text import unique_slug


class Game(models.Model):
    game = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True,
                            null=False, editable=False)

    @property
    def parameter_defaults(self):
        param_value_dict = {}

        parameters = self.parameters

        for param in parameters.all():
            param_value_dict[param.slug] = param.default_value.slug

        return param_value_dict

    def get_absolute_url(self):
        return reverse('games:game', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.game

    class Meta:
        ordering = ['game']


class GameScore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='game_scores'
    )
    game = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='game_scores'
    )
    parameter_values = models.ManyToManyField(
        'ParameterValue', related_name='game_scores'
    )
    score = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_high_score(self):
        return not self.__scores_with_same_param_settings().filter(score__gt=self.score).exists()

    @property
    def is_user_high_score(self):
        # requires testing
        return not self.__scores_with_same_param_settings() \
            .filter(score__gt=self.score, user=self.user).exists()

    def __scores_with_same_param_settings(self):
        scores = GameScore.objects.filter(game=self.game)
        for param_value in self.parameter_values.all():
            scores = scores.filter(
                parameter_values__value=param_value.value,
                parameter_values__parameter__slug=param_value.parameter.slug
            )

        return scores


class Parameter(models.Model):
    parameter = models.CharField(max_length=100)
    game = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='parameters'
    )
    slug = models.SlugField(max_length=50, unique=True,
                            null=False, editable=False)
    default_value = models.ForeignKey(
        'ParameterValue', on_delete=models.CASCADE, null=True, blank=True,
        related_name='parameters_as_default'
    )
    # values = models.ManyToManyField(
    #     'ParameterValue', related_name='parameter'
    # )

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.parameter


class ParameterValue(models.Model):
    value = models.CharField(
        max_length=50,
        help_text="Value should be uppercase word. Numbers must be less than 10 digits \
            without chars to order properly."
    )
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, related_name='values'
    )
    slug = models.SlugField(max_length=50, unique=True,
                            null=False, editable=False)
    ordering_name = models.CharField(max_length=50, editable=False, null=False)

    # @property
    # def attribute_value(self):
    #     return self.value.lower()

    def save(self, *args, **kwargs):
        if not self.slug:
            value = self.value
            self.slug = unique_slug(value, type(self))
        if not self.ordering_name:
            self.ordering_name = self.__generate_ordering_name()
        super().save(*args, **kwargs)

    def __generate_ordering_name(self):
        if self.value.isdigit():
            value = int(self.value)
            value = f'{value:09d}'
        else:
            value = self.value
        return value

    def __str__(self):
        return self.parameter.parameter + ': ' + self.value

    class Meta:
        ordering = ['parameter', 'ordering_name']
