from django.db.models import Q
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from tweets.models import Tweet
from .serializers import TweetSerializer
from .pagination import TweetsPagination

class TweetList(generics.ListAPIView):
	serializer_class = TweetSerializer
	pagination_class = TweetsPagination


	def get_serializer_context(self, *args, **kwargs):
		context = super(TweetList, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		requested_user = self.kwargs.get('username')
		if requested_user:
			queryset = Tweet.objects.filter(user__username=requested_user).order_by('-timestamp')
		else:
			is_follow = self.request.user.profile.get_following()
			queryset1 = Tweet.objects.filter(user__in=is_follow)
			queryset2 = Tweet.objects.filter(user=self.request.user)
			queryset = (queryset1 | queryset2).distinct().order_by('-timestamp')
		if self.request.GET.get('q'):
			queryset = queryset.filter(
				Q(content__icontains=self.request.GET.get('q')) |
				Q(user__username__icontains=self.request.GET.get('q'))
			)
		return queryset	


class TweetRetrieveAPIView(generics.RetrieveAPIView):
	serializer_class = TweetSerializer
	permission_classes = [permissions.IsAuthenticated]
	queryset = Tweet.objects.all()


class RetweetAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not Allowed"
		if tweet_qs.exists() and tweet_qs.count() == 1:
			tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
			if tweet is not None:
				data = TweetSerializer(tweet).data
				return Response(data)
			message = "Can not Retweet at the same day."
		return Response({"message": message}, status=404)


class LikeToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		tweet_qs = Tweet.objects.filter(pk=pk)
		message = "Not Allowed"
		if request.user.is_authenticated:
			tweet_like = Tweet.objects.like_toggle(request.user, tweet_qs.first())
			return Response({'liked': tweet_like})

		return Response({"message": message}, status=404)


class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)