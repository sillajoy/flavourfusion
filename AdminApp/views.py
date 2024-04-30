from django.shortcuts import render, redirect
from UserApp.models import UserModel,RecipePostModel


# Create your views for admin.
def dashboard(request):
    """
    Display the admin dashboard.

    If the request method is POST, toggle the status of a user based on the provided
    user ID. Then, redirect to the 'admin_dashboard' page.

    Retrieve statistics such as user count, recipe count, active user count, inactive
    user count, archived recipe count, and not archived recipe count. Also, retrieve
    the list of users and all recipes. Render the 'dashboard.html' template with the
    retrieved data.

    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = UserModel.objects.get(pk=user_id)
        # Toggle user status
        user.user_status = not user.user_status
        user.save()
        return redirect('admin_dashboard')
    
    # Retrieve statistics
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
    """
    Archive a recipe.

    If the request method is POST, archive the recipe with the provided recipe ID.
    Then, redirect to the 'admin_dashboard' page.

    """
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = RecipePostModel.objects.get(pk=recipe_id)
        # Archive the recipe
        recipe.is_archived = True
        recipe.save()
    return redirect('admin_dashboard')

def unarchive_recipe(request):
    """
    Unarchive a recipe.

    If the request method is POST, unarchive the recipe with the provided recipe ID.
    Then, redirect to the 'admin_dashboard' page.

    """
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = RecipePostModel.objects.get(pk=recipe_id)
        # Unarchive the recipe
        recipe.is_archived = False
        recipe.save()
    return redirect('admin_dashboard')
