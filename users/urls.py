from django.urls import path

from .views import MyAccountPageView, ReviewCreateView

from games.views import ScoreListView

app_name = 'users'
urlpatterns = [
    path('my-account/', MyAccountPageView.as_view(), name='my-account'),
    path('my-scores/', ScoreListView.as_view(), name='my-scores'),
    path('my-scores/<slug>/', ScoreListView.as_view(), name='my-scores'),
    path('review/create/', ReviewCreateView.as_view(), name='create-review'),
]
