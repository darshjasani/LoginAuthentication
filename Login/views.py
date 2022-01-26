from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from random import randint
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
            context={
                "User":True,
            }
            messages.info(request,'Please enter the username')
            return render(request,'login.html',context)
        elif password1 == '':
            context={
                'username':username1,
                'password':True,
            }
            messages.info(request,'Please enter the password')
            return render(request,'login.html',context)
        else :
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
    List = ['<','>','{','}','[',']','(',')','/']
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        checkpassword = request.POST.get('checkpassword')
        if username == '':
            context = {
                "User":True,
            }
            messages.info(request,'Please enter the username')
            #return redirect('signin')
            return render(request,'signin.html',context)
        elif email == '':
            context = {
                "email" : True,
                "username" : username,
            }
            messages.info(request,'Please enter the email id')
            return render(request,'signin.html',context)
        elif password == '':
            context = {
                "emailid" : email,
                "username" : username,
                "password":True,
            }
            messages.info(request,'Please enter the password')
            return render(request,'signin.html',context)
        elif checkpassword == '':
            context = {
                "emailid" : email,
                "username" : username,
                "password1":password,
                "checkpassword":True,
            }
            messages.info(request,'Please enter the check password')
            return render(request,'signin.html',context)
        elif password != checkpassword :
            context={
                "emailid":email,
                "username":username,
                "password1":password,
            }
            messages.info(request,'Passwords do not match. Enter Again')
            return render(request,'signin.html',context)
        elif username != '' and password == checkpassword:
            valid = [True if i in List else False for i in username]
            if True not in valid:
                if len(password) >= 8 and  any(i.isdigit() for i in password) and not password.isalnum() :
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
                    context={
                        "username":username,
                        "emailid":email,
                    }
                    messages.info(request,'Enter Password as per condition')
                    return render(request,'signin.html',context)
            else :
                messages.info(request,'Enter username correctly')
                return render(request,'signin.html')
        else :
            messages.info(request,'Enter Details Correctly')
    return render(request,'signin.html')

def logoutUser(request):
    logout(request)
    return render(request,'logout.html')

def forgetpwd(request):
    if request.method == "POST":
        global email
        email = request.POST.get('email')
        if email == "":
            context={
                "email":True,
            }
            messages.info(request,'Please enter the email id')
            return render(request,'forgetpwd.html',context)
        else :
            if not User.objects.filter(email=email).exists():
                messages.info(request,'Enter Registered Email ID')
                return render(request,'forgetpwd.html')
            global otp
            otp = randint(0000,9999)
            #messages.info(request,otp)
            subject = "OTP Number"
            message = "Your OTP is : "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            email_to = [email,]
            send_mail(subject,message,email_from,email_to)
            return render(request,'otppage.html')


    return render(request,'forgetpwd.html')

def otppage(request):
    if request.method == "POST":
        otp_got = request.POST.get('otp')
        if otp_got == "":
            context={
                "otp":True,
                "disabled":"none",
            }
            messages.info(request,'Please enter the otp')
            return render(request,'otppage.html',context)
        else :
            if otp_got.isdigit() :
                if int(otp_got) == otp :
                    messages.info(request,'Correct OTP')
                    return render(request,'resetpwd.html')
                else :
                    messages.info(request,'incorrect OTP')
            else :
                messages.info(request,'Please enter the otp correctly')
    return render(request,'otppage.html')

def resetpwd(request):
    if request.method =="POST":
        password = request.POST.get('password')
        checkpassword = request.POST.get('checkpassword')
        if password == '':
            context = {
                "password":True,
            }
            messages.info(request,'Please enter the password')
            return render(request,'resetpwd.html',context)
        elif checkpassword == '':
            context = {
                "password1":password,
                "checkpassword":True,
            }
            messages.info(request,'Please enter the check password')
            return render(request,'resetpwd.html',context)
        elif password != checkpassword :
            context={
                "password1":password,
            }
            messages.info(request,'Passwords do not match. Enter Again')
            return render(request,'resetpwd.html',context)
        else :
            if len(password) >= 8 and  any(i.isdigit() for i in password) and not password.isalnum() :
                    user = User.objects.get(email=email)
                    user.set_password(password)
                    user.save()
                    return render(request,'login.html')
            else :
                    messages.info(request,'Enter Password as per condition')
                    return render(request,'resetpwd.html')
    return render(request,'resetpwd.html')