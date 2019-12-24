from django.utils.timesince import timesince
from rest_framework import serializers
from accounts.api.serializers import UserSreializer
from tweets.models import Tweet


class ParentTweetSerializer(serializers.ModelSerializer):
	user = UserSreializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()

	class Meta:
		model = Tweet
		fields = [
			'id',
			'user',
			'content',
			'timestamp',
			'date_display',
			'timesince'
		]

	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d %Y, at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.timestamp)


class TweetSerializer(serializers.ModelSerializer):
	user = UserSreializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	parent = ParentTweetSerializer(read_only=True)

	class Meta:
		model = Tweet
		fields = [
			'id',
			'user',
			'content',
			'timestamp',
			'date_display',
			'timesince',
			'parent'
		]

	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d %Y, at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.timestamp)
