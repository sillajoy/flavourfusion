from django.shortcuts import render, redirect
from UserApp.models import UserModel,RecipePostModel


# Create your views for admin.
def dashboard(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = UserModel.objects.get(pk=user_id)
        if user.user_status:
            user.user_status = False 
        else:
            user.user_status = True
        user.save()
        return redirect('admin_dashboard')
    
    users = UserModel.objects.all()
    for user in users:
        user.post_count = RecipePostModel.objects.filter(user_id=user).count()

    user_count = UserModel.objects.count()
    recipe_count = RecipePostModel.objects.count()
    active_user_count = UserModel.objects.filter(user_status=True).count()
    inactive_user_count = UserModel.objects.filter(user_status=False).count()
    archive_recipe_count = RecipePostModel.objects.filter(is_archived=True).count()
    not_archived_recipe_count = RecipePostModel.objects.filter(is_archived=False).count()

    recipes = RecipePostModel.objects.all()
    return render(request, 'dashboard.html', {'users': users, 'user_count': user_count, 'recipe_count': recipe_count, 'active_user_count': active_user_count, 'inactive_user_count': inactive_user_count, 'recipes': recipes, 'archive_recipe_count': archive_recipe_count, 'not_archived_recipe_count': not_archived_recipe_count})

def archive_recipe(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = RecipePostModel.objects.get(pk=recipe_id)
        recipe.is_archived = True
        recipe.save()
    return redirect('admin_dashboard')

def unarchive_recipe(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = RecipePostModel.objects.get(pk=recipe_id)
        recipe.is_archived = False
        recipe.save()
    return redirect('admin_dashboard')
