from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import time
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    return redirect('login')

def loginUser(request):
    if request.method == 'POST':
        username1 = request.POST.get('name')
        password1 = request.POST.get('password')
        if username1 == '':
            messages.info(request,'Please enter the username')
            return render(request,'login.html')
        elif password1 == '':
            messages.info(request,'Please enter the password')
            return render(request,'login.html')
        user = authenticate(request,username=username1, password=password1)

        if user is not None:
            login(request,user)
            #messages.success(request,'Loged in successfully')
            #time.sleep(3)
            return redirect('/')
        
        else :
            messages.info(request,'Given username or passowrd is incorrect. Please enter again!!')

    return render(request,'login.html')

def signinUser(request):
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        checkpassword = request.POST.get('checkpassword')
        if username == '':
            messages.info(request,'Please enter the username')
            return render(request,'signin.html')
        elif email == '':
            messages.info(request,'Please enter the email id')
            return render(request,'signin.html')
        elif password == '':
            messages.info(request,'Please enter the password')
            return render(request,'signin.html')
        elif checkpassword == '':
            messages.info(request,'Please enter the check password')
            return render(request,'signin.html')
        elif password != checkpassword :
            messages.info(request,'Passwords do not match. Enter Again')
            return render(request,'signin.html')
        elif username != '' and password == checkpassword:
            if len(password) >= 8 and  not password.isdigit() :
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username already exists. Enter new username')
                    return render(request,'signin.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email Id already exists. Enter new Email Id')
                    return render(request,'signin.html')
                user =  User(username=username,email=email)
                user.set_password(password)
                user.save()
                return render(request,'login.html')
            else :
                messages.info(request,'Enter Password Correctly')
                return render(request,'signin.html')
        else :
            messages.info(request,'Enter Details Correctly')
    return render(request,'signin.html')

def logoutUser(request):
    logout(request)
    return render(request,'logout.html')