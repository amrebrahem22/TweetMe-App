from django.utils.timesince import timesince
from rest_framework import serializers
from accounts.api.serializers import UserSreializer
from tweets.models import Tweet


class ParentTweetSerializer(serializers.ModelSerializer):
	user = UserSreializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	did_liked = serializers.SerializerMethodField()

	class Meta:
		model = Tweet
		fields = [
			'id',
			'user',
			'content',
			'timestamp',
			'date_display',
			'timesince',
			'parent',
			'likes',
			'did_liked'
		]

	def get_did_liked(self, obj):
		request = self.context.get('request')
		user = request.user
		if user.is_authenticated:
			if user in obj.liked.all():
				return True
		return False


	def get_likes(self, obj):
		return obj.liked.all().count()

	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d %Y, at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.timestamp)


class TweetSerializer(serializers.ModelSerializer):
	parent_id = serializers.CharField(write_only=True, required=False)
	user = UserSreializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	parent = ParentTweetSerializer(read_only=True)
	likes = serializers.SerializerMethodField()
	did_liked = serializers.SerializerMethodField()

	class Meta:
		model = Tweet
		fields = [
			'parent_id',
			'id',
			'user',
			'content',
			'timestamp',
			'date_display',
			'timesince',
			'parent',
			'likes',
			'did_liked',
			'reply'
		]

	def get_did_liked(self, obj):
		request = self.context.get('request')
		user = request.user
		if user.is_authenticated:
			if user in obj.liked.all():
				return True
		return False


	def get_likes(self, obj):
		return obj.liked.all().count()

	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d %Y, at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.timestamp)
