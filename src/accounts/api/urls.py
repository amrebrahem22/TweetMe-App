from django.urls import path 
from tweets.api.views import TweetList

app_name = 'profile-tweets'

urlpatterns = [
	path('<username>/tweets/', TweetList.as_view(), name='list')
]
