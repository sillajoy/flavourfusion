from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserModel)
admin.site.register(MainCategoryModel)
admin.site.register(SubCategoryModel)
admin.site.register(EventModel)
admin.site.register(EventSubcategoryModel)
admin.site.register(RecipePostModel)
admin.site.register(TagsModel)
admin.site.register(PostIngredientsModel)
admin.site.register(ReviewModel)
admin.site.register(RecipePostCommentModel)
admin.site.register(RecipeImagesModel)
admin.site.register(ProcedureStep)
admin.site.register(NutritionFact)
admin.site.register(SavedRecipe)
admin.site.register(ShoppingListItem)
admin.site.register(Ingredients)