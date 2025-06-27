from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import User,PendingUser
from django.contrib import messages,auth
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from datetime import datetime,timezone
from common.tasks import send_email


# Create your views here.

def home(request: HttpRequest):
    return render(request,"home.html")

def login(request: HttpRequest):
    if request.method=="POST":
        email:str = request.POST.get("email")
        password:str = request.POST.get("password")

        user = auth.authenticate(request, email = email, password = password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged-in")
            return redirect("home")
        else:
            messages.error(request,"Invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")

def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request,"You are now logged-out.")
    return redirect("home")

def register(request: HttpRequest):
    if request.method=="POST":
        email : str = request.POST["email"]
        password : str = request.POST["password"]
        cleaned_email = email.lower()

        if User.objects.filter(email=cleaned_email).exists():
            messages.error(request,"Email exists on the platform")
            return redirect("register")
        else:
            verification_code=get_random_string(10)
            PendingUser.objects.update_or_create(
                email=cleaned_email,
                defaults={
                    "password": make_password(password),
                    "verification_code": verification_code,
                    "created_at": datetime.now(timezone.utc)
                }
            )
            send_email(
                "Verify Your Account",
                [cleaned_email],
                "emails/email_verification_template.html",
                context={'code': verification_code}
            )
            messages.success(request,f"Verification code sent to {cleaned_email}")
            return render(request,"verify_account.html",context={"email":cleaned_email})
        
    else:
        return render(request,"register.html")
    
def verify_account(request: HttpRequest):
    if request.method=="POST":
        code:str = request.POST["code"]
        email:str = request.POST["email"]
        pending_user = PendingUser.objects.filter(
            verification_code = code,
            email = email
        ).first()
        if pending_user and pending_user.is_valid():
            user = User.objects.create(
                email= pending_user.email,
                password = pending_user.password
            )
            pending_user.delete() #as pending_user is no longer required
            auth.login(request,user)
            messages.success(request,"Account verified. You are now logged-in.")
            return redirect("home") #yet to create its view

        else:
            messages.error(request,"Invalid or expired verification code")
            return render(request,"verify_account.html",{"email":email},status=400)