from django.urls import path
from django.views.generic.base import RedirectView
from .views import TweetsListView, TweetsCreateView, TweetDetailView, Retweet

app_name = "tweet"

urlpatterns = [
	path('', RedirectView.as_view(url="/"), name='index'),
	path('<pk>/', TweetDetailView.as_view(), name='detail'),
	path('<pk>/retweet/', Retweet.as_view(), name='retweet'),
	path('create/', TweetsCreateView.as_view(), name='create'),
]
