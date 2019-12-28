import re
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save 

from hashtags.signals import parsed_hashtags

User = settings.AUTH_USER_MODEL


class TweetManager(models.Manager):
	def retweet(self, user, parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj

		qs = self.get_queryset().filter(user=user, parent=og_parent).filter(
				timestamp__year=timezone.now().year,
				timestamp__month=timezone.now().month,
				timestamp__day=timezone.now().day,
			)

		if qs.exists():
			return None

		obj = self.model(
				parent=og_parent,
				user=user,
				content=og_parent
			)
		obj.save()

		return obj

	def like_toggle(self, user, tweet_obj):
		if user in tweet_obj.liked.all():
			is_liked = False
			tweet_obj.liked.remove(user)
		else:
			is_liked = True
			tweet_obj.liked.add(user)
		return is_liked


class Tweet(models.Model):
	parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.CharField(max_length=140)
	liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
	reply = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = TweetManager()

	def __str__(self):
		return self.content[:50]

	def get_absolute_url(self):
		return reverse('tweet:detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-timestamp']



def post_save_tweet_reciever(sender, instance, created, *args, **kwargs):
	if created:
		reg_user = r'@(P?<username>[\w.@+-]+)'
		username = re.findall(reg_user, instance.content)

		reg_hashtag = r'#(P?<hashtag>[\w\d-]+)'
		hashtags = re.findall(reg_hashtag, instance.content)

		parsed_hashtags.send(instance.__class__, hashtag_list=hashtags)


post_save.connect(post_save_tweet_reciever, sender=Tweet)
