from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from .models import Tweet
from .forms import TweetForm
from .mixins import FormUserNeededMixin


User = get_user_model()

# Create your views here.
def index(request):
	return render(request, 'base.html')

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        qs = None
        if query:
            qs = User.objects.filter(
                    Q(username__icontains=query)
                )
        context = {"users": qs}
        return render(request, "search.html", context)


class Retweet(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweet, pk=pk)
		if request.user.is_authenticated:
			new_tweet = Tweet.objects.retweet(request.user, tweet)
			return HttpResponseRedirect(tweet.get_absolute_url())
		return HttpResponseRedirect(tweet.get_absolute_url())


class TweetsListView(ListView):
	template_name = 'base.html'

	def get_queryset(self, *args, **kwargs):
		queryset = Tweet.objects.all()
		if self.request.GET.get('q'):
			queryset = queryset.filter(
				Q(content__icontains=self.request.GET.get('q')) |
				Q(user__username__icontains=self.request.GET.get('q'))
			)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = TweetForm()
		return context


class TweetDetailView(DetailView):
	model = Tweet
	template_name = 'single.html'


class TweetsCreateView(FormUserNeededMixin, CreateView):
	model = Tweet
	form_class = TweetForm
	template_name = 'base.html'


class TweetUpdateView(FormUserNeededMixin, UpdateView):
	model = Tweet
	form_class = TweetForm
	template_name = 'base.html'

