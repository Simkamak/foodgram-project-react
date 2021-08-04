from django.contrib import admin
from .models import Follow, Ingredient, Recipe, Tag
from import_export.admin import ImportMixin
from  .resources import IngredientResource


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name',)
    list_filter = ('author', 'name', 'tags')


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    list_filter = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    resource_class = IngredientResource


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)

