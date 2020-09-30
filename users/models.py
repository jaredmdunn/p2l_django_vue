from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse

import datetime
import pytz

from games.models import Game, Parameter, GameScore


class CustomUser(AbstractUser):
    dob = models.DateField(
        verbose_name="Date of Birth", null=True, blank=True
    )

# percentiles - from all scores in the game
# high score
# number improved within time frame

    def stats(self, game):
        # check if user has any scores for the game; if not, display message
        # for game in Game.objects.all():
        #     print(game.game_scores)
        #     # print(Game.game_scores.all)
        #     print('\n\n\n\n\n')
        # if Game.objects.game_scores.filter(user=self):
        #     pass

        stats = {}

        # number of high scores
        user_scores_list = GameScore.objects.prefetch_related('game').filter(
            game=game, user=self
        )
        num_high_scores = 0
        for score in user_scores_list:
            if score.is_high_score:
                num_high_scores += 1
        stats['Your high scores'] = num_high_scores

        # set up dates for improvement stats
        today = self.__datetime_x_days_ago(0)
        yesterday = self.__datetime_x_days_ago(1)
        last_week = self.__datetime_x_days_ago(7)

        # number improved in past day
        personal_bests_one_day = self.__count_personal_bests(
            yesterday, today, game
        )
        stats['New personal bests achieved today'] = personal_bests_one_day

        # number improved in past week
        personal_bests_one_week = self.__count_personal_bests(
            last_week, today, game
        )
        stats['New personal bests achieved within the last week'] = personal_bests_one_week

        return stats

    def __datetime_x_days_ago(self, x):
        # create today's date
        today = datetime.date.today()

        # create new datetime
        new_datetime = datetime.datetime.combine(
            datetime.date.today() - datetime.timedelta(days=x),
            datetime.datetime.max.time()
        ).replace(tzinfo=pytz.UTC)  # replace this to change timezone

        return new_datetime

    def __count_personal_bests(self, early_datetime, later_datetime, game):
        """Counts the number of high scores achieved between the dates

        Args:
            early_date (datetime): The earlier date
            later_date (datetime): The later date

        Returns:
            int: the count
        """
        early_personal_bests = self.__personal_bests_before(
            early_datetime, game)
        later_personal_bests = self.__personal_bests_before(
            later_datetime, game)

        count = 0
        for param_set in early_personal_bests:
            if later_personal_bests[param_set] > early_personal_bests[param_set]:
                count += 1

        return count

    def __personal_bests_before(self, end_datetime, game):
        """Finds the high scores before a certain date

        Args:
            date (datetime): The end date for the scores

        Returns:
            dict: A dictionary linking parameter to score
        """
        high_score = 0
        user_scores_list = GameScore.objects.prefetch_related('parameter_values').filter(
            game=game, user=self, created__lte=end_datetime
        )

        # build up dictionary of personal bests
        personal_bests_dict = {}
        for score in user_scores_list:
            # get hashable parameter values for use as key in personal_bests_dict
            score_params = tuple(score.parameter_values.all())
            score = score.score

            # if already has pb, compare, else add to personal best dict
            if score_params in personal_bests_dict:
                prev_high_score = personal_bests_dict[score_params]
                if score > prev_high_score:
                    personal_bests_dict[score_params] = score
            else:
                personal_bests_dict[score_params] = score

        return personal_bests_dict

    def get_absolute_url(self):
        return reverse('my-account')


class Review(models.Model):
    anonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    review = models.TextField(max_length=250)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )

    def get_absolute_url(self):
        return reverse('pages:homepage')

    def __str__(self):
        username = 'Anonymous' if self.anonymous else str(self.user)
        return '"' + self.review + '"\n- ' + username
