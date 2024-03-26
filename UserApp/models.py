from django.db import models

# User table 
class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='images/user_profile/', blank=True)
    user_bio = models.TextField(null=True, blank=True)
    user_password = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50, blank=True)
    user_email = models.CharField(max_length=50, blank=True)
    user_create_date = models.DateTimeField(auto_now_add=True)
    user_status = models.BooleanField(default=True)

    class Meta():
        db_table = 'user_table'

    def __str__(self):
        return f'{self.user_name}'

# Main Category table 
class MainCategoryModel(models.Model):
    main_category_id = models.AutoField(primary_key=True)
    main_category_name = models.CharField(max_length=100)

    class Meta():
        db_table = "main_category_table"

    def __str__(self):
        return f'{self.main_category_name}'

# Sub Category table
class SubCategoryModel(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=100)
    main_category_id = models.ForeignKey(MainCategoryModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "sub_category_table"

    def __str__(self):
        return f'{self.sub_category_name}'

# Event table
class EventModel(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_status = models.BooleanField(default=True)
    event_img = models.ImageField(upload_to='images/event_img/', null=True)

    class Meta():
        db_table = 'event_table'

    def __str__(self):
        return f'{self.event_name}'

# event subcategory table
class EventSubcategoryModel(models.Model):
    event_subcategory_id = models.AutoField(primary_key=True)
    event_subcategory_name = models.CharField(max_length=100, null=True)
    event_id = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    sub_category_id = models.ForeignKey(SubCategoryModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'event_subcategory_table'

    def __str__(self):
        return f'{self.event_subcategory_name}'


# Post table
class RecipePostModel(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=100)
    post_time_needed = models.CharField(max_length=50)
    post_difficulty_level = models.CharField(max_length=50, null=True)
    post_calories = models.CharField(max_length=100, null=True)
    post_description = models.TextField()
    post_additional_notes_by_chef = models.TextField(null=True, blank=True)
    recipe_image = models.ImageField(upload_to='images/recipe_img/')
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    event_id = models.ForeignKey(EventModel, on_delete=models.CASCADE, null=True, blank=True)
    sub_category_id = models.ForeignKey(SubCategoryModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'recipe_post_table'

    def __str__(self):
        return f'{self.post_title}'
    
# nutritional facts table
class NutritionFact(models.Model):
    Name = models.CharField(max_length=100, blank= True)
    Value = models.CharField(max_length=100, blank= True)
    post = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE, null=True)
    

    class Meta():
        db_table = 'nutrition_facts_table'

    def __str__(self):
        return f'{self.Name}- {self.post.post_title}'

# tags table
class TagsModel(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50)
    post_id = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'tags_table'

    def __str__(self):
        return f'{self.tag_name} - {self.post_id.post_title}'


# add ingredients to post
class PostIngredientsModel(models.Model):
    post_ingreds_id = models.AutoField(primary_key=True)
    post_ingredient_detail = models.TextField(null=True)
    post = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'postingredients_table'


# review table
class ReviewModel(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_overall = models.CharField(max_length=50, null=True)
    review = models.TextField()
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'review_table'

# post comment  
class RecipePostCommentModel(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField(null=True)
    post_id = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta():
        db_table = 'comment_table'

# recipe images
class RecipeImagesModel(models.Model):
    main_dish_image = models.ImageField(upload_to='images/post_img/')
    preparation_image = models.ImageField(upload_to='images/post_img/')
    final_result_image = models.ImageField(upload_to='images/post_img/')
    recipe = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE)


    class Meta():
        db_table ='recipe_images_table'

# cooking steps
class ProcedureStep(models.Model):
    step_order = models.IntegerField()
    step_text = models.TextField()
    recipe = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE, related_name='procedure_steps')

    class Meta():
        db_table = 'procedure_steps'

    def __str__(self):
        return f'{self.step_text}- {self.recipe.post_title}'

# saved recipes 
class SavedRecipe(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipe = models.ForeignKey(RecipePostModel, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        db_table ='saved_recipes'

    def __str__(self):
        return f'{self.recipe.post_title}'
    
# ingredients list grocery 
class Ingredients(models.Model):
    name = models.CharField(max_length=100)

    class Meta():
        db_table = 'ingredients'

    def __str__(self):
        return f'{self.name}'

# grocery shopping list    
class ShoppingListItem(models.Model):
    ingredient = models.ForeignKey(PostIngredientsModel, on_delete=models.CASCADE) 
    added_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)   

    class Meta():
        db_table ='shopping_list_items'

    def __str__(self):
        return self.ingredient.post_ingredient_detail