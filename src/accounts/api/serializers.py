from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers

User = get_user_model()

class UserSreializer(serializers.ModelSerializer):
	followers_count = serializers.SerializerMethodField()
	url = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'followers_count',
			'url'
		]

	def get_followers_count(self, obj):
		return 0

	def get_url(self, obj):
		return reverse_lazy('accounts:profile', kwargs={'username': obj.username})