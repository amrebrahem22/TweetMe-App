from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from .models import UserProfile

User = get_user_model()

class UserDetailView(DetailView):
	queryset = User.objects.all()
	template_name = 'tweet.html'

	def get_object(self):
		return get_object_or_404(User, username__iexact=self.kwargs.get('username'))


class UserFollow(View):
	def get(self, request, username, *args, **kwargs):
		user_qs = get_object_or_404(User, username__iexact=username)
		if request.user.is_authenticated:
			user_profile, created = UserProfile.objects.get_or_create(user=request.user)
			if user_qs in user_profile.following.all():
				user_profile.following.remove(user_qs)
			else:
				user_profile.following.add(user_qs)

		return redirect('accounts:profile', username=username)