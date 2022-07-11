from atexit import register
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class ProductPhotoInline(admin.StackedInline):
    model = ProductsPhoto
    max_num = 3
    extra = 0


class AnswerInline(admin.StackedInline):
    model = Answer
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
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug', 'available',)
    list_display_links = ('category',)
    search_fields = ('category',)
    list_editable = ('available',)
    list_filter = ('available',)
    prepopulated_fields = {"slug": ("category",)}
    save_on_top = True
    inlines = [SubcategoriesInline, ]


@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory', 'slug', 'available',)
    list_display_links = ('subcategory',)
    search_fields = ('subcategory', )
    list_editable = ('available',)
    list_filter = ('category', 'available', )
    prepopulated_fields = {"slug": ("subcategory",)}
    save_on_top = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('id', 'product', 'price', 'stock', 'available', )
    list_display_links = ('product',)
    search_fields = ('product', )
    list_editable = ('available',)
    list_filter = ('category', 'subcategory', 'available', )
    save_on_top = True
    inlines = [ProductDetailInline, ProductPhotoInline, ]

        
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('product', 'question', 'date_create')
    list_display_links = ('question',)
    search_fields = ('product', )
    #list_editable = ('display',)
    save_on_top = True
    inlines = [AnswerInline, ]


#admin.site.register(ProductsPhoto)
admin.site.register(Feedback)
admin.site.register(Answer)