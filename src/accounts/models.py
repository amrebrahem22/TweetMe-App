from django.db import models
from django.conf import settings

# for the reverse relationship "followed_by"
class UserProfileManager(models.Manager):
	use_for_related_fields = True

	def all(self):
		qs = self.get_queryset().all()
		try:
			if self.instance:
				qs = qs.exclude(user=self.instance)
		except:
			pass
		return qs

	def count(self):
		qs = self.get_queryset().all()
		try:
			if self.instance:
				qs = qs.exclude(user=self.instance)
		except:
			pass
		return qs.count()


class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
	following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by') # get users who i follow and the reverse will return users who following me

	objects = UserProfileManager()

	def __str__(self):
		return str(self.following.all().count())	

	# just for the following
	def get_following(self):
		qs = self.following.all()
		return qs.exclude(username=self.user.username)


