from django.urls import path

from .views import UserNameCountView

urlpatterns = [
    path('usernames/<username:username>/count/', UserNameCountView.as_view()),
]