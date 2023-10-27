from django.urls import path

from .views import UserNameCountView, RegisterView

urlpatterns = [
    path('usernames/<username:username>/count/', UserNameCountView.as_view()),
    path('register/', RegisterView.as_view())
]