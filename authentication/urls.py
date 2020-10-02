from django.urls import path
from authentication.views import RegistrationView,LoginView,UsernameValidationView,EmailValidationView
from django.views.decorators.csrf import csrf_exempt


app_name= 'authentication'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('validate-username/',csrf_exempt(UsernameValidationView.as_view()),name="usernameValidation"),
    path('validate-email/',csrf_exempt(EmailValidationView.as_view()),name="emailValidation"),
]