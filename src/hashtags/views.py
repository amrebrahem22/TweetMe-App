from django.shortcuts import render
from django.views.generic.base import View

from .models import Hashtag

class HashtagView(View):
	def get(self, request, hashtag, *args, **kwargs):
		tag, created = Hashtag.objects.get_or_create(tag=hashtag)
		return render(request, 'hashtag.html', {'hashtag': tag})
