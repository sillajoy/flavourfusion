from django.urls import path
from AdminApp import views
from . views import *

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'), 
    path('archive_recipe/', views.archive_recipe, name='archive_recipe'),
    path('unarchive_recipe/', views.unarchive_recipe, name='unarchive_recipe'),
]