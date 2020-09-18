from django.urls import path
from .views import AnagramGameView, MathGameView

app_name = 'games'
urlpatterns = [
    path('anagram/', AnagramGameView.as_view(), name='anagram'),
    path('math/', MathGameView.as_view(), name='math'),
]