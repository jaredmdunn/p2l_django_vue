from django.test import TestCase

from games.models import Game, GameScore, Parameter, ParameterValue
from users.models import CustomUser

import datetime
import mock


class TestStats(TestCase):

    def setUp(self):
        self.set_up_models()
        self.create_scores()
        self.add_params_to_scores()

        # fetch stats
        self.stats = self.user1.stats(self.game)
        self.day_stats = self.stats['Number of new personal bests achieved today']
        self.week_stats = self.stats['Number of new personal best achieved within the last week']

    def create_scores(self):
        # set up dates
        today = datetime.date.today()
        one_week_ago = today - datetime.timedelta(days=8)
        two_days_ago = today - datetime.timedelta(days=2)

        # one week ago
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = one_week_ago

            score_5_1w = GameScore.objects.create(
                user=self.user1, game=self.game, score=5
            )

        # two days ago
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = two_days_ago

            score_10_2d = GameScore.objects.create(
                user=self.user1, game=self.game, score=10
            )

        # today
        score_20_tdy = GameScore.objects.create(
            user=self.user1, game=self.game, score=20
        )

    def set_up_models(self):
        self.user1 = CustomUser.objects.create(username='1')
        self.user2 = CustomUser.objects.create(username='2')
        self.game = Game.objects.create(game='Math Facts')
        self.operation = Parameter.objects.create(
            parameter='Operation', game=self.game)
        self.max_number = Parameter.objects.create(
            parameter='Max Number', game=self.game
        )
        self.addition = ParameterValue.objects.create(
            value='Addition', parameter=self.operation
        )
        self.five = ParameterValue.objects.create(
            value='5', parameter=self.max_number
        )

    def add_params_to_scores(self):
        """Adds addition and 5 parameters to a score

        Args:
            score: The score to which parameters should be added
        """
        for score in GameScore.objects.all():
            score.parameter_values.add(self.addition)
            score.parameter_values.add(self.five)

    def test_day_stats(self):
        self.assertEqual(self.day_stats, 1)

    def test_week_stats(self):
        self.assertEqual(self.week_stats, 1)
