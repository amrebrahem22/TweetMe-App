from django.urls import path
from .views import TweetList, TweetCreateAPIView

urlpatterns = [
	path('', TweetList.as_view(), name='list'),
	path('create/', TweetCreateAPIView.as_view(), name='create'),
]