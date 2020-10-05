from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages,auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator

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

                domain=get_current_site(request).domain
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                link=reverse('authentication:activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

                activate_url="http://"+domain+link

                email_subject="Activate Your account"
                email_body="Hi "+user.username+" Please use this link to verify your account\n"+activate_url
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

    def post(self,request):
        username=request.POST['username']    
        password=request.POST['password']

        if username and password:
            user=auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,"Welcome "+user.username+" you are logged in!!")
                    return redirect('expenses:expenses')
                else:    
                    messages.error(request,"Account is not active,please check Your Email")
                    return render(request,'authentication/login.html',{}) 

            messages.error(request,"Invalid crediential,Try again")
            return render(request,'authentication/login.html',{})

        messages.error(request,"Please fill all the fields")
        return render(request,'authentication/login.html',{})

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.info(request,"you are logged out!!")
        return redirect('authentication:login')



class VerificationView(View):
    def get(self,request,uidb64,token):

        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not token_generator.check_token(user,token):
                return redirect('authentication:login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('authentication:login') 

            user.is_active=True
            user.save()

            messages.success(request,"Account Successfully activated") 
            return redirect('authentication:login')
        except Exception as ex:
            pass    

        return redirect('authentication:login')        

