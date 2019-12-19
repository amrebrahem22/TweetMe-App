from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.CharField(max_length=140)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.content[:50]

	def get_absolute_url(self):
		return reverse('tweet:index')

