from django.urls import path
from . import views

urlpatterns=[
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('register/',views.register,name="register"),
    path('verify-account/', views.verify_account,name="verify_account"),
]