from django.urls import path

from .views import UserNameCountView, RegisterView,LoginView

urlpatterns = [
    path('usernames/<username:username>/count/', UserNameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
]