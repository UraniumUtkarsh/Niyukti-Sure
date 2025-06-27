from django.urls import reverse
from django.test.client import Client
from accounts.models import PendingUser
from django.contrib.auth.hashers import check_password

def test_register_user(client):
    url = reverse("register")
    request_data={
        "email":"test1@ns.com",
        "password":"123"
    }
    response = client.post(url,request_data)
    assert response.status_code == 200
    pending_user = PendingUser.objects.filter(email=request_data["email"]).first()
    assert pending_user
    assert check_password(request_data["password"], pending_user.password)
    ...

def test_register_user_duplicate_email():
    ...

def test_verify_account_valid_code():
    ...

def test_verify_account_invalid_code():
    ...

def test_login_valid_credentials():
    ...

def test_login_invalid_credentials():
    ...

