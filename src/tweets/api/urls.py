from django.urls import path
from .views import (
	TweetList, 
	TweetCreateAPIView, 
	# TweetRetrieveAPIView, 
	RetweetAPIView, 
	LikeToggleAPIView,
	TweetDetailList
)

urlpatterns = [
	path('', TweetList.as_view(), name='list'),
	path('create/', TweetCreateAPIView.as_view(), name='create'),
	path('<pk>/', TweetDetailList.as_view(), name='detail'),
	path('<pk>/retweet/', RetweetAPIView.as_view(), name='retweet'),
	path('<pk>/like/', LikeToggleAPIView.as_view(), name='like-toggle'),
	
]