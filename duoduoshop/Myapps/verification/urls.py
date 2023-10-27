from django.urls import path
from .views import ImageCodeView, CmsCodeView
urlpatterns = [
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile:mobile>/', CmsCodeView.as_view()),

]