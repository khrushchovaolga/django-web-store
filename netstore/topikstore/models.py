from distutils.command.upload import upload
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Categories(models.Model):
    category = models.CharField(max_length=250, verbose_name=_('Category'))
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='URL')
    is_public = models.BooleanField(default=True, verbose_name = _('Is public'))

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        index_together = (('id', 'slug'),)


class Subcategories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name = 'subcats', verbose_name = _('Category'))
    subcategory = models.CharField(max_length=250, verbose_name=_('Subcategory'))
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='URL')
    is_public = models.BooleanField(default=True, verbose_name=_('Is public'))

    def __str__(self):
        return self.subcategory

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.slug})

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')
        index_together = (('id', 'slug'),)


class Brands(models.Model):
    brand = models.CharField(max_length=250, verbose_name=_('Brand'))
    slug = models.SlugField(max_length=250, verbose_name='URL')
    is_public = models.BooleanField(default=True, verbose_name=_('Is public'))

    def __str__(self):
        return self.brand


class Sizes(models.Model):
    size = models.CharField(max_length=25, verbose_name=_('Size'))
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.size


class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name='catproducts', verbose_name=_('Category'))
    subcategory = models.ForeignKey(Subcategories, on_delete = models.PROTECT, related_name='subcatproducts', verbose_name=_('Subcategory'))
    brand = models.ForeignKey(Brands, on_delete=models.PROTECT, related_name='brands', verbose_name=_('Brand'))
    product = models.CharField(max_length=250, verbose_name=_('Product'))
    short_description = models.TextField(blank=False, verbose_name=_('Short description'))
    full_description = models.TextField(blank=False, verbose_name=_('Full description'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    size = models.ForeignKey(Sizes, on_delete=models.PROTECT, verbose_name=_('Size'))
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock'))
    available = models.BooleanField(default=True, verbose_name=_('Is available'))
    data_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    data_updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    image = models.ImageField(upload_to = 'products', verbose_name=_('Photo'))

    def get_absolute_url(self):
        return reverse('product', kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.subcategory.slug, 'product_pk': self.pk})
    
    def __str__(self):
        return f'{self.product} {self.size}'

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductsPhoto(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images', verbose_name=_('Product'))
    photo = models.ImageField(upload_to = 'products/', verbose_name=_("Product's image"))

    def __str__(self):
        return str(self.product)


class ProductDetail(models.Model):
    product = models.OneToOneField(Products, on_delete=models.CASCADE, related_name='detail', primary_key=True, verbose_name=_('Product'))
    terms = models.TextField(blank=True, verbose_name=_('Terms of use'))
    composition = models.TextField(blank=False, verbose_name=_('Composition'))
    ph = models.FloatField(null=True, verbose_name='PH')
    contraindications = models.CharField(max_length=300, verbose_name=_('Contraindications'))
    storage_conditions = models.TextField(blank=True, verbose_name=_('Storage conditions'))
    age_category = models.CharField(max_length=100, verbose_name=_("Age's category"))
    expiration_date = models.CharField(max_length=300, verbose_name=_('Expiration date')) 


class ProductFeedbacks(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='feedbacks',verbose_name=_('Product'))
    author_name = models.CharField(max_length=100, verbose_name=_("Author's name"))
    feedback = models.TextField(blank=False, verbose_name=_('Feedback'))
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    is_public = models.BooleanField(default=True, verbose_name=_('Is public'))

    def __str__(self):
        return self.feedback

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')
        ordering = ['-date_create']


class ProductQuestions(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name=_('Product'), related_name='questions')
    author_name = models.CharField(max_length=100, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_('Email'))
    question = models.TextField(blank=False, verbose_name=_('Question'))
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    is_public = models.BooleanField(default=True, verbose_name=_('Is public'))

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['-date_create']


class Answers(models.Model):
    question = models.OneToOneField(ProductQuestions, on_delete=models.CASCADE, verbose_name=_('Question'), related_name='answer', primary_key = True)
    answer = models.TextField(blank = False, verbose_name=_('Answer'))
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    date_update = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        ordering = ['-date_create']