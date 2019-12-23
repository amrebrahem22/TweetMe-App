from django.db import models
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models.signals import post_save

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

	# toggle Follow
	def toggle_follow(self, user, to_follow):
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		if to_follow in user_profile.following.all():
			user_profile.following.remove(to_follow)
			added = False
		else:
			user_profile.following.add(to_follow)
			added = True
		return added

	# Is Following
	def is_following(self, user, user_following):
		user_profile, created = UserProfile.objects.get_or_create(user=user)
		if user_following in user_profile.following.all() or created:
			return True
		return False


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

	def get_follow_url(self):
		return reverse_lazy('accounts:follow', kwargs={'username': self.user.username})

	def get_absolute_url(self):
		return reverse_lazy('accounts:profile', kwargs={'username': self.user.username})



def post_save_profile(sender, instance, created, *args, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(post_save_profile, sender=settings.AUTH_USER_MODEL)