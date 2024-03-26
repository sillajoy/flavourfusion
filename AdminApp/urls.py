from django.urls import path
from AdminApp import views
from . views import *

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'), 
]