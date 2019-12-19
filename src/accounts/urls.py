from django.urls import path
from .views import UserDetailView

app_name = 'accounts'

urlpatterns = [
	path('<username>/', UserDetailView.as_view(), name='profile'),
]

