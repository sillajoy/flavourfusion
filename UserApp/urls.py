from django.urls import path
from UserApp import views
from . views import *


urlpatterns = [
    path('', views.home, name='home_page'), 
    path('christmas_recipes', views.christmas, name='christmas_page'),
    path('home/<int:sub_category_id>/', views.home, name='home_page_with_subcategory'),
    path('detail', views.view, name='details'),
    path('title/<int:recipe_id>', views.view, name='view_recipe'),
    path('details', views.view2, name='details2'),
    path('about', views.about, name='about'),
    path('feedback', views.submit_feedback, name='feedback'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='user_logout'),
    path('profile', views.profile, name='profile'),
    path('update', views.update_user, name='update_profile'),
    path('saved/<int:id>/', views.save, name='save'),
    path('saved_recipes', views.saved_recipes, name='saved'),
    path('deletesaved/<int:id>', views.delete_saved_recipe, name='delete_saved_recipe'),
    path('search/', views.search_view, name='search'),
    path('add_new_recipe', views.add_new_recipe, name='add_new_recipe'),
    path('delete_user_recipe/<int:id>', views.delete_user_recipe, name="delete_user_recipe"),
    path('update_details/<int:id>', views.recipe_update_details, name='recipe_update_details'),
    path('grocery', views.grocery, name='grocery'),
    path('add_ingredients', views.add_ingredients, name='add_ingredients'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('register_new_user', views.register_new_user, name='register_user'),
    path('userprofile/<int:id>/', views.user_profile, name='user_profile'),
    path('archive/<int:post_id>/', views.archive_recipe_post, name='archive_recipe_post'),
    path('archived', views.archived_recipe_post, name='archived_recipe_post'),
    path('unarchive/<int:post_id>/', views.unarchive_recipe_post, name='unarchive_recipe_post'),
]
