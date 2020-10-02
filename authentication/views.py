from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages

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
        messages.success(request,"success")
        messages.warning(request,"warning")
        messages.error(request,"Error")
        return render(request,'authentication/register.html',{})

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html',{})

