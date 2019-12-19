from django.db.models import Q
from rest_framework import permissions
from rest_framework import generics
from .serializers import TweetSerializer
from tweets.models import Tweet

class TweetList(generics.ListAPIView):
	serializer_class = TweetSerializer

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