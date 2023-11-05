from django.urls import path

from .views import UserNameCountView, RegisterView, LoginView, LogoutView, CenterView, EmailView, VerifyEmailView
from .views import AddressCreateView, AddressView, AddressModifyView, DefaultAddressView, AddressTitleModifyView
from .views import PasswordmodifyView
from utils.converters import AddressIdConverter, UsernameConverter
from django.urls import register_converter
register_converter(AddressIdConverter, 'address_id')
register_converter(UsernameConverter, 'username')
urlpatterns = [
    path('usernames/<username:username>/count/', UserNameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', VerifyEmailView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
    path('addresses/<address_id:address_id>/', AddressModifyView.as_view()),
    path('addresses/<address_id:address_id>/default/', DefaultAddressView.as_view()),
    path('addresses/<address_id:address_id>/title/', AddressTitleModifyView.as_view()),
    path('password/', PasswordmodifyView.as_view()),
]