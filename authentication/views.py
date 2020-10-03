from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.

class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'User name should be AlphaNumeric'},status=400)
        if User.objects.filter(username=username):
            return JsonResponse({'username_error':'Sorry! User name already exist,Choose another name'},status=409)    

        return JsonResponse({'username_valid':True})

class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email):
            return JsonResponse({'email_error':'Sorry! Email name already exist,Choose another name'},status=409)    

        return JsonResponse({'email_valid':True})            




class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html',{})

    def post(self,request):
        username=request.POST['username']
        email_get=request.POST['email']
        password=request.POST['password']

        context={'fieldValues':request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email_get).exists():
                if len(password)<6:
                    messages.error(request,"Password is too short")
                    return render(request,'authentication/register.html',context)
                user=User.objects.create_user(username=username,email=email_get)
                user.set_password(password)
                user.is_active=False
                user.save()
                email_subject="Activate Your account"
                email_body="Test"
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@gmail.com',
                    [email_get],)
                email.send(fail_silently=False)
                messages.success(request,"Account Successfully Created")
                return render(request,'authentication/register.html',{})
        return render(request,'authentication/register.html',{})

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html',{})

