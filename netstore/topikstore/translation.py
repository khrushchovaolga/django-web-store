from dataclasses import fields
from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Categories)
class CategoriesTranslationOptions(TranslationOptions):

    'Translation for model: Categories'

    fields = ('category', )


@register(Subcategories)
class SubcategoriesTranslationOptions(TranslationOptions):

    'Translation for model: Subcategories'

    fields = ('subcategory', )


@register(Products)
class ProductsTranslationOptions(TranslationOptions):

    'Translation for model: Products'

    fields = ('product', 'short_description', 'full_description', )


@register(ProductDetail)
class ProductDetailTranslationOprions(TranslationOptions):

    'Translation for model: ProductDetail'

    fields = ('terms', 'contraindications', 'storage_conditions', 'expiration_date', )