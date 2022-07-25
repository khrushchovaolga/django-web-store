from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


class ProductPhotoInline(admin.StackedInline):
    model = ProductsPhoto
    max_num = 3
    extra = 0


class AnswersInline(admin.StackedInline):
    model = Answers
    max_num = 1
    extra = 0


class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    max_num = 1
    extra = 0


class SubcategoriesInline(admin.StackedInline):
    model = Subcategories
    max_num = 100
    extra = 5
    prepopulated_fields = {"slug": ("subcategory", )}


@admin.register(Categories)
class CategoriesAdmin(TranslationAdmin):
    list_display = ('category', 'slug', 'is_public', )
    list_display_links = ('category', )
    search_fields = ('category', )
    list_editable = ('is_public', )
    list_filter = ('is_public', )
    prepopulated_fields = {"slug": ("category", )}
    save_on_top = True
    inlines = [SubcategoriesInline, ]


@admin.register(Subcategories)
class SubcategoriesAdmin(TranslationAdmin):
    list_display = ('category', 'subcategory', 'slug', 'is_public',)
    list_display_links = ('subcategory', )
    search_fields = ('subcategory', )
    list_editable = ('is_public', )
    list_filter = ('category', 'is_public', )
    prepopulated_fields = {"slug": ("subcategory", )}
    save_on_top = True


@admin.register(Products)
class ProductsAdmin(TranslationAdmin):
    list_display = ('product', 'price', 'stock', 'available', )
    list_display_links = ('price',)
    search_fields = ('product', )
    list_editable = ('available',)
    list_filter = ('category', 'subcategory', 'available', )
    save_on_top = True
    inlines = [ProductDetailInline, ProductPhotoInline, ]


@admin.register(ProductDetail)
class ProductDetailAdmin(TranslationAdmin):
    list_display = ('product', )
    list_display_links = ('product', )

        
@admin.register(ProductQuestions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('product', 'question', 'date_create')
    list_display_links = ('question',)
    search_fields = ('product', )
    save_on_top = True
    inlines = [AnswersInline, ]


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'slug')
    list_display_links = ('brand',)
    search_fields = ('brand', )
    save_on_top = True
    prepopulated_fields = {"slug": ("brand", )}


admin.site.register(Sizes)