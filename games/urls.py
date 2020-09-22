from django.urls import path
from .views import GameDetailView, save_score

app_name = 'games'
urlpatterns = [
    path('<slug>/', GameDetailView.as_view(), name='game'),
    path('<slug>/save-score/', save_score, name='save-score'),
]