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
		queryset = Tweet.objects.all().order_by('-timestamp')
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