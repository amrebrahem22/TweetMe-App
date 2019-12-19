from django.urls import path
from django.views.generic.base import RedirectView
from .views import TweetsListView, TweetsCreateView

app_name = "tweet"

urlpatterns = [
	path('', RedirectView.as_view(url="/"), name='index'),
	path('create/', TweetsCreateView.as_view(), name='create'),
]
