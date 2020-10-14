from django.urls import path
from .views import GameDetailView, ScoreListView, save_score #,AnagramGameView

app_name = 'games'
urlpatterns = [
    #path('game/vue/<slug>/', AnagramGameView.as_view(), name='vue-game'),
    path('game/<slug>/', GameDetailView.as_view(), name='game'),
    path('game/<slug>/save-score/', save_score, name='save-score'),
    path('leaderboards/', ScoreListView.as_view(), name='leaderboards'),
    path('leaderboards/<slug>/', ScoreListView.as_view(), name='leaderboards'),
]
