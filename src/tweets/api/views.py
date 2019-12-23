from django.db.models import Q
from rest_framework import permissions
from rest_framework import generics
from tweets.models import Tweet
from .serializers import TweetSerializer
from .pagination import TweetsPagination

class TweetList(generics.ListAPIView):
	serializer_class = TweetSerializer
	pagination_class = TweetsPagination

	def get_queryset(self):
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


class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)