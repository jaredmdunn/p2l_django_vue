from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse

import datetime

from games.models import Game, Parameter, GameScore, GameScoreParameters

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
        # number improved in past day
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        personal_bests_one_day = self.__count_personal_bests(yesterday, today, game)
        # number improved in past week
        last_week = today - datetime.timedelta(days=7)
        personal_bests_one_week = self.__count_personal_bests(last_week, today, game)
        
        return {
            'Number of new personal bests achieved today': personal_bests_one_day,
            'Number of new personal best achieved within the last week': personal_bests_one_week,
        }

    def __count_personal_bests(self, early_date, later_date, game):
        """Counts the number of high scores achieved between the dates

        Args:
            early_date (datetime): The earlier date
            later_date (datetime): The later date

        Returns:
            int: the count
        """
        early_personal_bests = self.__personal_bests_before(early_date, game)
        later_personal_bests = self.__personal_bests_before(later_date, game)

        count = 0
        for param_set in early_personal_bests:
            if later_personal_bests[param_set] > early_personal_bests[param_set]:
                count += 1

        return count

    def __personal_bests_before(self, date, game):
        """Finds the high scores before a certain date

        Args:
            date (datetime): The end date for the scores

        Returns:
            dict: A dictionary linking parameter to score
        """
        high_score = 0
        user_scores_list = GameScore.objects.filter(game=game, user=self)

        personal_bests_dict = {}
        for score in user_scores_list:
            if score.created.date() < date:
                game_score_param_list = []

                for game_score_param in score.game_score_parameters:
                    game_score_param_list.append((game_score_param.parameter,game_score_param.value))

                if personal_bests_dict.has_key(game_score_param_list):
                    prev_high_score = personal_bests_dict(game_score_param_list)
                    if score.value > prev_high_score:
                        personal_bests_dict[game_score_param_list] = score.value
                else:
                    personal_bests_dict[game_score_param_list] = score.value
        
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
