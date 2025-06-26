from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import User,PendingUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from datetime import datetime,timezone
from common.tasks import send_email


# Create your views here.

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
                "email/email_verification_template.html",
                context={'code': verification_code}
            )
            messages.success(request,f"Verification code sent to {cleaned_email}")
            return render(request,"verify_account.html")
        
    else:
        return render(request,"register.html")