from django.urls import path
from .views import UserDetailView, UserFollow

app_name = 'accounts'

urlpatterns = [
	path('<username>/', UserDetailView.as_view(), name='profile'),
	path('<username>/follow/', UserFollow.as_view(), name='follow'),
]

