from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages 
from webdev import settings
from django.core.mail import send_mail
import random
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password

def checknum (s):
    for i in s:
        if(i.isdigit()):
            return True
    return False


@csrf_exempt
def _login(request):
    if(request.method=='POST'):
        username = request.POST['username']
        passw = request.POST['passinfo']

        user = authenticate(username=username, password=passw)

        if user is not None:
            login(request,user)
            context = {
            'user': request.user
            }
            return redirect('/')
        else :
            messages.error(request,"Username or password is incorrect")

    return render(request, 'signin.html')

@csrf_exempt
def _signup(request):
    template = loader.get_template('register.html')
    name = None
    if(request.method=='POST' and request.POST['passinfo'] and request.POST['emailinfo']) and request.POST['passinfo'] and request.POST['username']:
        
        username = request.POST['username']
        passw = request.POST['passinfo']
        passw2 = request.POST['passinfo2']
        mail = request.POST['emailinfo']

        if User.objects.filter(username=username):
            context = {
            'email': mail,
            'username': username,
            'message': 'The username already exists !!'
            }
            return HttpResponse(template.render(context))
        
        if User.objects.filter(email=mail):
            context = {
            'email': mail,
            'username': username,
            'message': 'The email already exists !!'
            }
            return HttpResponse(template.render(context))
        if len(passw) < 8 or checknum(passw) == 0:
            context = {
            'email': mail,
            'message': 'Password must container at least 8 characters and 1 number.'
            }
            return HttpResponse(template.render(context))
        if passw != passw2:
            context = {
            'email': mail,
            'message': "Password didn't match."
            }
            return HttpResponse(template.render(context))

        myuser = User.objects.create_user(username ,mail, passw)
        messages.success(request,"Your account had been created")
        myuser.save()
        return redirect('login')
    
    context = {
    'username':name
    }
    return HttpResponse(template.render(context))

@csrf_exempt
def _logout(request):
    logout(request)
    return redirect('/')

def makepass():
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    newpass = charset[random.randint(52,len(charset)-1)]
    for i in range(7):
        newpass += charset[random.randint(0,len(charset)-1)]
    return newpass
    
@csrf_exempt
def _passforgot(request):
    template = loader.get_template('forgotpassword.html')
    if(request.method=='POST'):
        mail = request.POST['emailinfo']
        user = User.objects.filter(email=mail)
        if user is not None:
            subject = "YOUR NEW PASSWORD"
            newpass = makepass()
            print(request.POST)
            user[0].set_password(newpass)
            user[0].save()
            message = 'Hello ' + user[0].username +'!!\n' + 'Here your new password: ' + newpass
            to_list = [user[0].email]
            from_email = settings.EMAIL_HOST_USER
            #send_mail(subject,message,from_email,to_list,fail_silently=True)
            messages.success(request,"Your password had been seed to your email") 
            return redirect('login')
        else:
            context = {
            'message': "Email not exitst"
            }
            return HttpResponse(template.render(context))
    return HttpResponse(template.render())

