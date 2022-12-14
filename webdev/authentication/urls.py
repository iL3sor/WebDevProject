from django.urls import path
from . import views

urlpatterns = [
    path('login', views._login, name='login'),
    path('signup', views._signup, name='signup'),
    path('passforgot', views._passforgot, name='passforgot'),
    path('logout', views._logout, name='logout'),
]