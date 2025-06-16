from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import User,PendingUser
from django.contrib import messages
from django.utils.crypto import get_random_string


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
            PendingUser.objects.create(
                email=cleaned_email
            )
    else:
        return render(request,"register.html")