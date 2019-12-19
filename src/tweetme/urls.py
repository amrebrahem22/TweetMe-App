from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from tweets.views import TweetsListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TweetsListView.as_view(), name="index"),
    path('tweet/', include('tweets.urls', namespace="tweet")),
    path('api/tweets/', include('tweets.api.urls'))
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)