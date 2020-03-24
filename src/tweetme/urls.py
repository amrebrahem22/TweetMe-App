from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from tweets.views import TweetsListView, SearchView
from hashtags.views import HashtagView

from tweets.api.views import SearchTweetList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TweetsListView.as_view(), name="index"),
    re_path(r'^tags/(?P<hashtag>.*)/$', HashtagView.as_view(), name="hashtag"),
    path('tweet/', include('tweets.urls', namespace="tweet")),
    path('search/', SearchView.as_view(), name='search'),
    path('api/tweets/', include('tweets.api.urls')),
    path('', include('accounts.urls', namespace='accounts')),
    path('api/tweet/', include('accounts.api.urls', namespace='profile-tweets')),
    path('api/search/', SearchTweetList.as_view(), name='search-api'), 
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)