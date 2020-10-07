from django.urls import path
from .views import GameDetailView, save_score, ScoreListView, AnagramGameView

app_name = 'games'
urlpatterns = [
    path('anagram-hunt/', AnagramGameView.as_view(), name='anagram-game'),
    path('<slug>/', GameDetailView.as_view(), name='game'),
    path('<slug>/save-score/', save_score, name='save-score'),
    path('leaderboards/<slug>/', ScoreListView.as_view(), name='leaderboards'),
]
