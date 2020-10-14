import json

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from common.utils.text import unique_slug


class Game(models.Model):
    """A model representing a game

    Fields:
        description: a description of the game
        game: the name of the game
        slug: a unique slug for the game
    """
    class GameType(models.IntegerChoices):
        VANILLA = 1
        VUE = 2

    description = models.TextField(blank=True, null=True)
    game = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True,
                            null=False, editable=False)
    type = models.PositiveSmallIntegerField(choices=GameType.choices, default=GameType.VANILLA)

    @property
    def parameter_defaults(self) -> dict:
        """A dictionary of default parameter values

        Returns:
            dict: a dictionary of parameter slugs to their default values
        """
        param_value_dict = {}

        parameters = self.parameters

        for param in parameters.all():
            default_param = param.default_value or param.values.first()
            param_value_dict[param.slug] = default_param.slug

        return param_value_dict

    def get_absolute_url(self):
        return reverse('games:game', args=[self.slug])

    def save(self, *args, **kwargs):
        """Overwrites save to initialize the slug"""
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.game

    class Meta:
        ordering = ['game']


class GameScore(models.Model):
    """A model representing a score for a game

    Fields:
        created: the date when the score was created
        game: a foreign key of the game
        parameter_values: a many to many field of parameter values
        score: the points scored
        user: a foreign key of the user
    """
    created = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='game_scores'
    )
    parameter_values = models.ManyToManyField(
        'ParameterValue', related_name='game_scores'
    )
    score = models.PositiveIntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='game_scores'
    )

    @property
    def is_high_score(self) -> bool:
        """Returns True if the score is a new high score. False, otherwise."""
        return not self._scores_with_same_param_settings().filter(score__gt=self.score).exists()

    @property
    def is_user_high_score(self):
        """Returns True if the score is a new high score among the user's scores."""
        return not self._scores_with_same_param_settings() \
            .filter(score__gt=self.score, user=self.user).exists()

    def _scores_with_same_param_settings(self):
        """Returns a QuerySet of game scores with the same parameter settings."""
        scores = GameScore.objects.filter(game=self.game)
        for param_value in self.parameter_values.prefetch_related('parameter'):
            scores = scores.filter(
                parameter_values__value=param_value.value,
                parameter_values__parameter__slug=param_value.parameter.slug
            )

        return scores


class Parameter(models.Model):
    """A model representing a parameter type (i.e. Max Number or Operation)

    Fields:
        default_value: a foreign key of the default parameter value
        game: a foreign key of the game
        parameter: the name of the parameter
        slug: a unique slug
    """
    default_value = models.ForeignKey(
        'ParameterValue', on_delete=models.CASCADE, null=True, blank=True,
        related_name='parameters_as_default'
    )
    game = models.ForeignKey(
        'Game', on_delete=models.CASCADE, related_name='parameters'
    )
    parameter = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True,
                            null=False, editable=False)

    def save(self, *args, **kwargs):
        """Overwrites save to generate a unique slug"""
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.game}: {self.parameter}'


class ParameterValue(models.Model):
    """A model representing a specific value for a parameter (i.e. 5 or Addition)

    Fields:
        ordering_name: the name used to order the parameters, generated during saving so 
            that numbers will order correctly (otherwise 11 comes before 2)
        parameter: a foreign key of the parameter
        slug: a unique slug
        value: the value for the parameter
    """
    ordering_name = models.CharField(max_length=50, editable=False, null=False)
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, related_name='values'
    )
    slug = models.SlugField(max_length=50, unique=True,
                            null=False, editable=False)
    value = models.CharField(
        max_length=50,
        help_text="Value should be uppercase word. Numbers must be less than 10 digits \
            without chars to order properly."
    )

    def save(self, *args, **kwargs):
        """Overwrites save to generate unique slug and a sortable ordering name"""
        if not self.slug:
            self.slug = unique_slug(self.value, type(self))

        if not self.ordering_name:
            self.ordering_name = self._generate_ordering_name()

        super().save(*args, **kwargs)

    def _generate_ordering_name(self):
        """Generates ordering name such that numbers will be 9 digits long with leading zeroes"""
        if self.value.isdigit():
            value = int(self.value)
            return f'{value:09d}'

        return self.value

    def __str__(self):
        return f'{self.parameter.parameter}: {self.value}'

    class Meta:
        ordering = ['parameter', 'ordering_name']
