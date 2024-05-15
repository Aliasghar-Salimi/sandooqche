from django.urls import path
from .views import home, RegisterView, whoami

app_name = 'users'
urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('whoami/', whoami, name='whoami'),
]
