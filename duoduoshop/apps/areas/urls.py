from django.urls import path

from .views import AreaView, SubAreaView

urlpatterns = [
    path('areas/', AreaView.as_view()),
    path('areas/<pk>/', SubAreaView.as_view()),
]