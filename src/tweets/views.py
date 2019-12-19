from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q

from .models import Tweet
from .forms import TweetForm
from .mixins import FormUserNeededMixin


# Create your views here.
def index(request):
	return render(request, 'base.html')


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


class TweetsCreateView(FormUserNeededMixin, CreateView):
	model = Tweet
	form_class = TweetForm
	template_name = 'base.html'


class TweetUpdateView(FormUserNeededMixin, UpdateView):
	model = Tweet
	form_class = TweetForm
	template_name = 'base.html'

