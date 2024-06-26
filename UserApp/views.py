from collections import Counter
import json
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.db.models import Q
from datetime import date
from AdminApp.models import *
from  UserApp.models import *
from django.contrib import messages

def home(request, sub_category_id=None):
    """
    View function for rendering the home page with recipe posts and recommendations.

    Returns:
        HttpResponse: Rendered home page with recipe posts and recommendations.
    """
    if 'user_id' in request.session:
        try:
            user_id = request.session['user_id']
            user = UserModel.objects.get(pk=user_id)
            viewed_post_subcategory_list = request.session.get(f'viewed_post_subcategory_list_{user.user_name}', [])

            if viewed_post_subcategory_list:
                most_common_subcategory_id = Counter(viewed_post_subcategory_list).most_common(1)[0][0]
                recommended_recipes = RecipePostModel.objects.filter(sub_category_id=most_common_subcategory_id, is_archived=False)[:3]
            else:
                recommended_recipes = None
        except UserModel.DoesNotExist:
            user = None
            recommended_recipes = None
    else:
        viewed_post_subcategory_list = request.COOKIES.get('viewed_post_subcategory_list')
        if viewed_post_subcategory_list:
            try:
                viewed_post_subcategory_list = json.loads(viewed_post_subcategory_list)
                most_common_subcategory_id = Counter(viewed_post_subcategory_list).most_common(1)[0][0]
                recommended_recipes = RecipePostModel.objects.filter(sub_category_id=most_common_subcategory_id, is_archived=True)[:3]
            except:
                recommended_recipes = None
        else:
            recommended_recipes = None

        
    main_categories = MainCategoryModel.objects.prefetch_related('subcategorymodel_set')
    active_event = EventModel.objects.filter(event_status=True).first()
    current_date = date.today()
    ads = AdsModel.objects.filter(ads_end_date__gte=current_date)
    
    selected_subcategory = None
    recipes = None
    
    if sub_category_id:
        selected_subcategory = SubCategoryModel.objects.filter(sub_category_id=sub_category_id).first()
        if selected_subcategory:
            recipes = RecipePostModel.objects.filter(sub_category_id=sub_category_id, is_archived=False)
        else:
            return render(request, 'home.html', {'recipes': None, 'selected_subcategory_name': None, 'main_categories': main_categories, 'active_event': active_event, 'ads': ads, 'recommended_recipes': recommended_recipes})
    else:
        recipes = RecipePostModel.objects.filter(is_archived=False).order_by('?')[:9] 
        
    return render(request, 'home.html', {'recipes': recipes, 'selected_subcategory_name': selected_subcategory.sub_category_name if selected_subcategory else None, 'sub_category': selected_subcategory, 'main_categories': main_categories, 'active_event': active_event, 'ads': ads, 'recommended_recipes': recommended_recipes})



def search_view(request):
    """
    Display search results for recipes.

    Retrieve the search query from the POST request. If a query is provided,
    search for recipes with titles, authors, or subcategory names containing
    the query text. Otherwise, return an empty queryset. Render the 'searched.html'
    template with the search results, all main categories, and all subcategories.

    Returns:
        HttpResponse: Rendered 'searched.html' template with search results, main categories, 
        subcategories, and search query.
    """
    query = request.POST.get('search')
    main_categories = MainCategoryModel.objects.all()
    subcategories = SubCategoryModel.objects.all()

    results = RecipePostModel.objects.filter(is_archived=False)

    if query:
        results = results.filter(
            Q(post_title__icontains=query) | Q(user_id__user_name__icontains=query) | Q(sub_category_id__sub_category_name__icontains=query)
        )
    
    for category in main_categories:
        category_filter = request.POST.get(f'category_filter_{category.main_category_id}')
        if category_filter and category_filter.isdigit():
            results = results.filter(sub_category_id=category_filter)

    return render(request, 'searched.html', {'results': results, 'main_categories': main_categories, 'query': query, 'subcategories': subcategories})



def christmas(request):
    """
    Display recipes associated with the Christmas event.

    Retrieve the Christmas event instance and all recipes associated with
    it. Then, render the 'christmas.html' template with the event instance
    and recipes.

    """
    event_instances = EventModel.objects.filter(event_name='Christmas').first() 
    recipes = RecipePostModel.objects.filter(event_id=event_instances, is_archived=False)

    context = {
        'event_instance': event_instances,
        'recipes': recipes,
    }
    return render(request, 'christmas.html', context)


def about(request):
    """
    Display information about the website.

    Render the 'about.html'

    """
    reviews = ReviewModel.objects.all()
    return render(request, 'about.html', {'reviews': reviews})


def view(request, recipe_id):
    """
    Display details of a recipe post.

    Retrieve the recipe details and associated images based on the recipe ID.
    If the user is authenticated, update the viewed post subcategory list in the session.
    If not authenticated, update the viewed post subcategory list in the cookies.
    Render the 'recipe_details1.html' template with the recipe details and images.

    """
    recipe = get_object_or_404(RecipePostModel, pk=recipe_id)
    images = RecipeImagesModel.objects.filter(recipe=recipe_id)
    

    user = None
    storage_type = None

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            user = None
            return HttpResponse("User does not exist")

        viewed_post_subcategory_list = request.session.get(f'viewed_post_subcategory_list_{user.user_name}', [])
        viewed_post_subcategory_list.append(recipe.sub_category_id.sub_category_id)
        request.session[f'viewed_post_subcategory_list_{user.user_name}'] = viewed_post_subcategory_list
        storage_type = "session"
    else:
        viewed_post_subcategory_list = request.COOKIES.get('viewed_post_subcategory_list', '[]')
        viewed_post_subcategory_list = json.loads(viewed_post_subcategory_list)
        viewed_post_subcategory_list.append(recipe.sub_category_id.sub_category_id)
        response = render(request, 'recipe_details1.html', {'recipes': recipe, 'images': images})
        response.set_cookie('viewed_post_subcategory_list', json.dumps(viewed_post_subcategory_list))
        storage_type = "cookie"


    if storage_type == "cookie":
        return response
    else:
        return render(request, 'recipe_details1.html', {'recipes': recipe, 'images': images})


def view2(request):
    """
    Display details of a recipe post and handle comments.

    If the request method is POST, retrieve the recipe details and associated information
    based on the provided post ID. Additionally, handle new comments submitted by users.
    Render the 'recipe_details2.html' template with the recipe details, procedure steps,
    additional notes, nutrition facts, ingredients, tags, comments, and the post ID.

    If the request method is not POST, redirect to the homepage.
    """
    if request.method == 'POST':
        post_id = request.POST.get('id') 
        recipe = get_object_or_404(RecipePostModel, pk=post_id)
        procedure_steps = ProcedureStep.objects.filter(recipe=recipe).order_by('step_order')
        additional_notes = recipe.post_additional_notes_by_chef
        nutrition_facts = NutritionFact.objects.filter(post=recipe)
        ingredients = PostIngredientsModel.objects.filter(post=recipe)
        tags = TagsModel.objects.filter(post_id=recipe)
        comments = RecipePostCommentModel.objects.filter(post_id=recipe)

        new_comment_text = request.POST.get('comment')
        postid = request.POST.get('id')
        if new_comment_text:
            if 'user_id' in request.session:
                user_id = request.session['user_id']
                user = UserModel.objects.filter(user_id=user_id).first()
                if user:
                    comment = RecipePostCommentModel()
                    post_instance = get_object_or_404(RecipePostModel, pk=postid)
                    comment.post_id = post_instance
                    comment.comment = new_comment_text
                    comment.user_id = user
                    comment.save()

        return render(request, 'recipe_details2.html', {
            'recipe': [recipe],
            'procedure_steps': procedure_steps,
            'additional_notes': additional_notes,
            'nutrition_facts': nutrition_facts,
            'ingredients': ingredients,
            'tags': tags,
            'comments': comments,
            'post_id': post_id,  
        })
    else:
        return redirect('/')



def login(request):
    """
    Log in the user or admin with provided credentials.

    If the request method is POST, attempt to authenticate the user
    or admin with the provided username and password based on the
    'login_type' parameter. If authentication is successful, set the
    'user_id' or 'admin_id' in the session accordingly and redirect to
    the URL specified by the 'next' parameter in the request, or to the
    homepage ('/') if no 'next' parameter is provided. If authentication
    fails or if the request method is not POST, render the 'login_new.html'
    template.

    """
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')
        if login_type == 'user':
            user = UserModel.objects.filter(user_name=username, user_password=password).first()
            if user:
                request.session['user_id'] = user.user_id
                return redirect('/')
        
        elif login_type == 'admin':
            admin = AdminModel.objects.filter(admin_username=username, admin_password=password).first()
            if admin:
                request.session['admin_id'] = admin.admin_id
                return redirect('admin_dashboard')

    return render(request, 'login_new.html')


def register_new_user(request):
    """
    Register a new user with provided credentials.

    If the request method is POST, attempt to register a new user
    with the provided username and password. If registration is
    successful, set the 'user_id' in the session to the newly created
    user's ID and redirect to the homepage ('/'). If the request method
    is not POST, render the 'register.html' template.

    """
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = UserModel()
        user.user_name = username
        user.user_password = password
        user.save()
        request.session['user_id'] = user.user_id    
        return redirect('/')
    return render(request,'register.html')



def logout(request):
    """
    Log out the user and redirect to the login page.

    If the user is logged in (i.e., 'user_id' is in the session),
    remove the 'user_id' from the session to log the user out. Then,
    redirect to the '/login' URL.

    """
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/login')


def profile(request):
    """
    Display the profile page for the logged-in user.

    If the user is logged in, retrieve the user's information and their
    recipe posts. Then, render the 'profile.html' template with the user's
    details and the count of their recipe posts. If the user is not logged
    in, redirect to the login page.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserModel.objects.filter(user_id=user_id).first()
        
        user_recipe_posts = RecipePostModel.objects.filter(user_id=user, is_archived=False)
        archive_recipe_posts = RecipePostModel.objects.filter(user_id=user, is_archived=True)        
        user_recipe_posts_count = user_recipe_posts.count()

        return render(request, 'profile.html', {'user': [user], 'user_recipe_posts': user_recipe_posts, 'user_recipe_posts_count': user_recipe_posts_count, 'archive_recipe_posts': archive_recipe_posts})
    else:
        return redirect('/login')

def update_user(request):
    """
    Update user profile information.

    If the user is logged in, retrieve the user's information and display
    the 'update_user.html' template. If the request method is POST, update
    the user's profile information based on the provided data. Redirect to
    the profile page after successful update. If the user is not logged in,
    redirect to the login page.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserModel.objects.filter(user_id=user_id).first()

        if request.method == 'POST':
            user.user_name = request.POST.get('username')
            user.user_password = request.POST.get('userpassword')
            user.user_phone = request.POST.get('userphone')
            user.user_email = request.POST.get('useremail')
            
            updated_bio = request.POST.get('userbio')
            if updated_bio:
                user.user_bio = updated_bio
            user_image = request.FILES.get('userimage')
            if user_image:
                user.user_image = user_image

            user.save()
            return redirect('/profile') 

    return render(request, 'update_user.html', {'user': user})


    
def delete_user_recipe(request, id):
    """
    Delete a recipe post belonging to the logged-in user.

    Retrieve the recipe post based on the provided ID. If the user is
    logged in and the recipe post belongs to the user, delete the recipe
    post and redirect to the profile page. If the user is not logged in
    or the recipe post does not belong to the user, redirect to the
    profile page without performing any action.

    """
    recipe = RecipePostModel.objects.get(post_id=id)
    recipe.delete()
    return redirect('/profile')
    
def save(request, id):
    """
    Save a recipe for the logged-in user.

    If the user is logged in and the recipe hasn't been saved already,
    create a new entry in the SavedRecipe table associating the recipe
    with the user. Then, redirect to the '/saved_recipes' URL.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        # Check if the recipe already saved
        if not SavedRecipe.objects.filter(user_id=user_id, recipe_id=id).exists():
            saved_recipe = SavedRecipe(user_id=user_id, recipe_id=id)
            saved_recipe.save()
    return redirect('/saved_recipes')

def saved_recipes(request):
    """
    Save a recipe for the logged-in user.

    If the user is logged in and the recipe hasn't been saved already,
    create a new entry in the SavedRecipe table associating the recipe
    with the user. Then, redirect to the '/saved_recipes' URL.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        saved_recipes = SavedRecipe.objects.filter(user_id=user_id)

        return render(request, 'saved.html', {'saved_recipes': saved_recipes})
    else:
        return render(request, 'login.html')
    
def delete_saved_recipe(request, id):
    """
    Delete a saved recipe. Redirects to '/saved_recipes' after deletion. Raises: Http404: If the saved recipe does not exist or does not belong to the user.
    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        saved_recipe = get_object_or_404(SavedRecipe, user_id=user_id, id=id)
        saved_recipe.delete()
    return redirect('/saved_recipes')


def add_new_recipe(request):
    """
    Add a new recipe post.

    If the user is logged in, retrieve the user's information, available subcategories,
    and events. If the request method is POST, save the recipe details, nutritional facts,
    ingredients, cooking procedure, images, and tags submitted in the form. Finally, redirect
    to the profile page. If the user is not logged in or if the request method is not POST,
    render the 'add_new_recipe.html' template with the available subcategories and events.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserModel.objects.get(user_id=user_id)
        subcategories = SubCategoryModel.objects.all()
        events = EventModel.objects.all()

        if request.method == 'POST':
            title = request.POST.get('title')
            time = request.POST.get('time')
            difficulty = request.POST.get('difficulty')
            calorie = request.POST.get('calorie')
            description = request.POST.get('description')
            notes = request.POST.get('notes')
            image = request.FILES.get('image_url')

            event_id = request.POST.get('event')
            if event_id:
                event = EventModel.objects.get(event_id=event_id)
            else:
                event = None
            subcategory_instance = SubCategoryModel.objects.get(sub_category_id=request.POST.get('subcategory'))

            # Save recipe details
            new_recipe = RecipePostModel(
                post_title=title,
                post_time_needed=time,
                post_difficulty_level=difficulty,
                post_calories=calorie,
                post_description=description,
                post_additional_notes_by_chef=notes,
                recipe_image=image,
                user_id=user,
                event_id=event,
                sub_category_id=subcategory_instance
            )
            new_recipe.save()

            # Save nutritional facts
            calorie_fact = NutritionFact(Name='Calories', Value=calorie, post=new_recipe)
            calorie_fact.save()
            protein_fact = NutritionFact(Name='Protein', Value=request.POST.get('protein'), post=new_recipe)
            protein_fact.save()
            carb_fact = NutritionFact(Name='Carbohydrates', Value=request.POST.get('carb'), post=new_recipe)
            carb_fact.save()
            fat_fact = NutritionFact(Name='Fat', Value=request.POST.get('fat'), post=new_recipe)
            fat_fact.save()
            sodium_fact = NutritionFact(Name='Sodium', Value=request.POST.get('sodium'), post=new_recipe)
            sodium_fact.save()
            cholesterol_fact = NutritionFact(Name='Cholesterol', Value=request.POST.get('cholesterol'), post=new_recipe)
            cholesterol_fact.save()

            # save ingredients information
            post_id = new_recipe.post_id
            for key, value in request.POST.items():# Iterate over the ingredients submitted in the form
                # Check if the input field is an ingredient field
                if key.startswith('ingredient'):
                    ingredient_detail = value

                    ingredient_obj = PostIngredientsModel(
                        post_ingredient_detail=ingredient_detail,
                        post_id=post_id
                    )
                    ingredient_obj.save()

            # save cooking procedure
            cooking_steps = [value for key, value in request.POST.items() if key.startswith('cooking_step')]

            for index, step_text in enumerate(cooking_steps, start=1):
                procedure_step = ProcedureStep(
                    step_order=index,
                    step_text=step_text,
                    recipe=new_recipe
                )
                procedure_step.save()

            # add images 
            image1 = request.FILES.get('main_dish_image')
            image2 = request.FILES.get('preparation_image')
            image3 = request.FILES.get('final_result_image')

            recipe_images = RecipeImagesModel()
            recipe_images.main_dish_image = image1
            recipe_images.preparation_image = image2
            recipe_images.final_result_image = image3
            recipe_images.recipe = new_recipe
            recipe_images.save()   

            # Save tags
            tags_data = request.POST.get('tags_data')
            if tags_data:
                tags = tags_data.split(',')
                for tag_name in tags:
                    tag = TagsModel(tag_name=tag_name, post_id=new_recipe)
                    tag.save()
            return redirect('/profile')

    return render(request, 'add_new_recipe.html', {'subcategories': subcategories, 'events': events})

def recipe_update_details(request, id):
    """
    Update details of a recipe.

    Retrieve the recipe post based on the provided ID. If the request method is POST,
    update the recipe details, nutritional facts, ingredients, cooking procedure, images,
    and tags based on the provided data. Finally, redirect to the profile page.

    """
    recipe = get_object_or_404(RecipePostModel, post_id=id)  

    if request.method == 'POST':
        # recipe details update
        recipe.post_title = request.POST.get('title')
        recipe.post_description = request.POST.get('description')
        recipe.post_additional_notes_by_chef = request.POST.get('notes')
        recipe.post_calories = request.POST.get('calorie')
        recipe.post_time_needed = request.POST.get('time')
        recipe.post_difficulty_level = request.POST.get('difficulty')
        event_id = request.POST.get('event')
        if event_id:
            event = EventModel.objects.get(event_id=event_id)
        else:
            event = None
        recipe.event_id = event

        subcategory_id = request.POST.get('subcategory')
        subcategory_instance = SubCategoryModel.objects.get(sub_category_id=subcategory_id)
        recipe.sub_category_id = subcategory_instance

        if 'image_url' in request.FILES:
            recipe.recipe_image = request.FILES['image_url']
        recipe.save()

        # nutritional facts update
        for fact in NutritionFact.objects.filter(post=recipe):
            updated_value = request.POST.get(fact.Name)
            if updated_value is not None:
                fact.Value = updated_value
                fact.save()

        # ingredients update
        new_ingredients = request.POST.getlist('ingredients')  # Get list of ingredients from form
        existing_ingredients = list(PostIngredientsModel.objects.filter(post=recipe))

        # Update existing ingredients
        for i, existing_ingredient in enumerate(existing_ingredients):
            if i < len(new_ingredients):
                existing_ingredient.post_ingredient_detail = new_ingredients[i]
                existing_ingredient.save()

        # Procedure steps update
        new_steps = request.POST.getlist('steps') 
        existing_steps = list(ProcedureStep.objects.filter(recipe=recipe).order_by('step_order'))

        for i, new_step in enumerate(new_steps):
            if i < len(existing_steps):
                # Update existing step
                existing_step = existing_steps[i]
                existing_step.step_text = new_step
                existing_step.save()

        # update images
        images_instance = RecipeImagesModel.objects.filter(recipe=recipe).first()
        if images_instance is not None:
            if 'main_dish_image' in request.FILES:
                images_instance.main_dish_image = request.FILES['main_dish_image']
            if 'preparation_image' in request.FILES:
                images_instance.preparation_image = request.FILES['preparation_image']
            if 'final_result_image' in request.FILES:
                images_instance.final_result_image = request.FILES['final_result_image']
            images_instance.save()

        # update tags for the recipe
        new_tags_data = request.POST.get('tags_data')
        new_tags = new_tags_data.split(',')

        # Fetch the existing tags from the database
        existing_tags = list(TagsModel.objects.filter(post_id=recipe.post_id))

        # Update existing tags and create new tags if necessary
        for i, new_tag in enumerate(new_tags):
            if i < len(existing_tags):
                # Update existing tag
                existing_tag = existing_tags[i]
                existing_tag.tag_name = new_tag
                existing_tag.save()
            else:
                new_tag_instance = TagsModel(tag_name=new_tag, post_id=recipe)
                new_tag_instance.save()

        return redirect('/profile')


    subcategories = SubCategoryModel.objects.all()
    events = EventModel.objects.all()
    nutrition_facts = NutritionFact.objects.filter(post=recipe)
    ingredients = PostIngredientsModel.objects.filter(post=recipe)
    cooking_procedure = ProcedureStep.objects.filter(recipe=recipe)
    images = RecipeImagesModel.objects.filter(recipe=recipe)
    tags = TagsModel.objects.filter(post_id=recipe)
    context = {'recipe': recipe, 'subcategories': subcategories, 'events': events, 'nutrient_facts': nutrition_facts, 'postingredients': ingredients, 'cooking_procedure': cooking_procedure, 'images': images, 'tags': tags}

    return render(request, 'update_recipe.html', context)


def grocery(request):
    """
    Display the grocery list for the logged-in user.

    If the user is logged in, retrieve the shopping list items associated with the user.
    Group the items by recipe. Finally, render the 'grocery.html' template with the grouped
    items. If the user is not logged in, redirect to the login page.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        list_items = ShoppingListItem.objects.filter(user_id=user_id)
        # Group items by recipe
        recipe_items = {}
        for item in list_items:
            recipe_title = item.ingredient.post.post_title
            if recipe_title not in recipe_items:
                recipe_items[recipe_title] = []
            recipe_items[recipe_title].append(item)
        
        # ingredients = Ingredients.objects.all()

        return render(request, 'grocery.html', {'recipe_items': recipe_items})
    else:
        return render(request, 'login.html')


def add_ingredients(request):
    """
    Add ingredients to the user's shopping list.

    If the user is logged in and the request method is POST, retrieve the ingredient ID
    from the POST data and add the corresponding ingredient to the user's shopping list.
    Then, render the 'grocery.html' template with the updated shopping list items grouped
    by recipe. If the user is not logged in, redirect to the login page.

    """
    if 'user_id' in request.session:
        if request.method == 'POST':
            ingredient_id = request.POST.get('ingredient_id')
            user_id = request.session['user_id']

            # Fetch the PostIngredientsModel instance corresponding to the ingredient_id
            ingredient = get_object_or_404(PostIngredientsModel, pk=ingredient_id)

            # Check if the ingredient is already in the user's shopping list
            existing_item = ShoppingListItem.objects.filter(user_id=user_id, ingredient=ingredient).first()
            if existing_item is None:
                item = ShoppingListItem(user_id=user_id, ingredient=ingredient)
                item.save()

        user_id = request.session.get('user_id')
        list_items = ShoppingListItem.objects.filter(user_id=user_id)
        # Group items by recipe
        recipe_items = {}
        for item in list_items:
            recipe_title = item.ingredient.post.post_title
            if recipe_title not in recipe_items:
                recipe_items[recipe_title] = []
            recipe_items[recipe_title].append(item)

        # ingredients = Ingredients.objects.all()

        return render(request, 'grocery.html', {'recipe_items': recipe_items})


def delete_item(request, item_id):
    """
    Delete an item from the user's shopping list.

    If the user is logged in, delete the shopping list item with the provided ID.
    Then, redirect to the 'grocery' page. If the user is not logged in, no action
    is taken.

    """
    if 'user_id' in request.session:
        ShoppingListItem.objects.filter(pk=item_id).delete()
        messages.success(request, 'Ingredient deleted successfully.')
    return redirect('grocery')


def user_profile(request, id):
    """
    Display the profile page for a specific user.

    Retrieve the user information and their recipe posts based on the provided user ID.
    Then, render the 'user_profile.html' template with the user's details and the count
    of their recipe posts.

    """
    user = UserModel.objects.get(user_id=id)
    user_recipe_posts = RecipePostModel.objects.filter(user_id=user, is_archived=False)
    user_recipe_posts_count = user_recipe_posts.count()
    return render(request, 'user_profile.html', {'user': user, 'user_recipe_posts': user_recipe_posts, 'user_recipe_posts_count': user_recipe_posts_count})


def submit_feedback(request):
    """
    Submit feedback from the user.

    If the request method is POST, retrieve the rating and feedback from the form data.
    If the user is logged in, associate the feedback with the user and save it to the database.
    Then, redirect to the '/about' page. If the user is not logged in, redirect to the login page.
    If the request method is not POST, render the 'feedback.html' template.

    """
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            user = UserModel.objects.filter(user_id=user_id).first()
            if user:
                review = ReviewModel(review_overall=rating, review=feedback, user_id=user)
                review.save()
                return redirect('/about')  
            else:
                return redirect('/login')  
        else:
            return redirect('/login') 

    return render(request, 'feedback.html')

def archive_recipe_post(request, post_id):
    """
    Archive a recipe post.

    If the user is logged in, archive the recipe post with the provided ID by setting
    its 'is_archived' attribute to True. Then, redirect to the '/profile' page.

    """
    recipe_post = get_object_or_404(RecipePostModel, pk=post_id)

    recipe_post.is_archived = True
    recipe_post.save()

    return redirect('/profile')

def archived_recipe_post(request):
    """
    Display archived recipe posts for the logged-in user.

    If the user is logged in, retrieve the archived recipe posts associated with the user
    and render the 'archived.html' template with the archived recipe posts. If the user
    is not logged in, redirect to the login page.

    """
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = UserModel.objects.filter(user_id=user_id).first()
        archived_recipe_posts = RecipePostModel.objects.filter(user_id=user, is_archived=True)

        return render(request, 'archived.html', {'archived_recipe_posts': archived_recipe_posts})
    else:
        return redirect('/login')
    
def unarchive_recipe_post(request, post_id):
    """
    Unarchive a recipe post.

    If the user is logged in, unarchive the recipe post with the provided ID by setting
    its 'is_archived' attribute to False. Then, redirect to the '/profile' page.

    """
    recipe_post = get_object_or_404(RecipePostModel, pk=post_id)

    recipe_post.is_archived = False
    recipe_post.save()

    return redirect('/profile')