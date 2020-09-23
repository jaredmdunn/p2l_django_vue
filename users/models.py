from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse

from datetime import datetime

from games.models import Game, Parameter, GameScore, GameScoreParameters

class CustomUser(AbstractUser):
    dob = models.DateField(
        verbose_name="Date of Birth", null=True, blank=True
    )

# percentiles - from all scores in the game
# high score
# number improved within time frame

    @property
    def stats(self):
        # check if user has any scores for the game; if not, display message
        if Game.game_scores.filter(user=user)
        # number improved in past day
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        high_scores_one_day = __count_high_scores(yesterday, today)
        # number improved in past week
        last_week = today - datetime.timedelta(days=7)
        high_scores_one_week = __count_high_scores(last_week, today)
        
        pass

    def __high_scores_before(self, date):
        high_score = 0
        user_scores_list = Game.game_scores.filter(user=user)

        high_scores_dict = {}
        for score in user_scores_list:
            if score.created.date < date.date:
                game_score_param_list = []

                for game_score_param in score.game_score_parameters:
                    game_score_param_list.append((game_score_param.parameter_id,game_score_param.value))

                if high_scores_dict.has_key(game_score_param_list):
                    prev_high_score = high_scores_dict(game_score_param_list)
                    if score.value > prev_high_score:
                        high_scores_dict[game_score_param_list] = score.value
                else:
                    high_scores_dict[game_score_param_list] = score.value
        
        return high_scores_dict


    def __count_high_scores(self, early_date, later_date):
        early_high_scores = __high_scores_before(early_date)
        later_high_scores = __high_scores_before(later_date)

        count = 0
        for param_set in early_high_scores:
            if later_high_scores[param_set] > early_high_scores[param_set]:
                count += 1

        return count

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
