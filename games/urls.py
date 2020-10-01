from django.urls import path
from .views import GameDetailView, save_score, ScoreListView

app_name = 'games'
urlpatterns = [
    path('<slug>/', GameDetailView.as_view(), name='game'),
    path('<slug>/save-score/', save_score, name='save-score'),
    path('leaderboards/<slug>/', ScoreListView.as_view(), name='leaderboards'),
]
