from tkinter import CASCADE
from tkinter.ttk import Widget
from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField
from django.urls import reverse


class Categories(models.Model):
    category = models.CharField(max_length=250, verbose_name='Категория')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, verbose_name='url')
    available = models.BooleanField(default=True, verbose_name = 'Наличие')

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        #для улучшения представления запросов
        index_together = (('id', 'slug'),)


class Subcategories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name = 'subcats',verbose_name = 'Категория')
    subcategory = models.CharField(max_length=250, verbose_name='Подкатегория')
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='url', unique=True)
    available = models.BooleanField(default=True, verbose_name = 'Наличие')

    def __str__(self):
        return self.subcategory

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.slug})

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        #для улучшения представления запросов
        index_together = (('id', 'slug'),)

class Product(models.Model):
    BRANDS = (
        ('Scalp', 'Scalp'),
        ('Sane', 'Sane'),
    )

    VOLUME = (
        ('40ml', '40ml'),
        ('50ml', '50ml'),
        ('75ml', '75ml'),
        ('100ml', '100ml'),
        ('200ml', '200ml'),
        ('250ml', '250ml'),
        ('500ml', '500ml')
    )

    category = models.ForeignKey(Categories, on_delete=models.PROTECT, related_name = 'catproducts', verbose_name = 'Категория')
    subcategory = models.ForeignKey(Subcategories, on_delete = models.PROTECT, related_name = 'subcatproducts', verbose_name='Подкатегория')
    brand = models.CharField(max_length=200, choices=BRANDS, verbose_name='Бренд')
    product = models.CharField(max_length=250, verbose_name='Название продукта')
    articul = models.CharField
    mini_description = models.TextField(blank=False, verbose_name='Краткое описание')
    big_description = models.TextField(blank=False, verbose_name = 'Полное описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    volume = models.CharField(max_length=50, choices=VOLUME, verbose_name="Об'єм")
    stock = models.PositiveIntegerField(default=0, verbose_name='Запас')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    image = models.ImageField(upload_to = 'products/', verbose_name = 'Заставка')
    #image2 = models.ImageField(upload_to = 'products/', verbose_name = 'Заставка 2')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    data_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновлення')


    def get_absolute_url(self):
        return reverse('product', kwargs={'cat_slug': self.category.slug, 'subcat_slug': self.subcategory.slug, 'product_pk': self.pk})
    
    def __str__(self):
        return f'{self.product} {self.volume}'


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductsPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Картинки')
    photo = models.ImageField(upload_to = 'products/', verbose_name='Фото товара')

    def __str__(self):
        return str(self.product)

class ProductDetail(models.Model):

    ROOLS = [
        ('Волосся', (
            ('Нанести невелику кількість шампуню на вологе волосся, зпінити, ретельно змити теплою водою. За необхідності повторити процедуру.', 'Шампунь'),
            ('Нанести невелику кількість бальзаму на чисте вологе волосся, рівномірно розподілити та злегка помасувати. Залишити на 2-3 хвилини, потім змити теплою водою.', "Бальзам"),
            ('Невелику кількість маски нанести на чисте вологе волосся та шкіру голови, рівномірно розподілити та злегка помасувати. Залишити на 5-7 хвилин, після чого змити теплою водою.', 'Маска'),
        )
    )
    ]
    AGES = [
        ('16+', 'З 16 років'),
        ('18+', 'З 18 років'),
        ('21+', 'З 21 року'),
    ]


    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail', primary_key=True, verbose_name='Продукт')
    rools_of_use = models.CharField(max_length=300, choices=ROOLS, verbose_name='Правила використання для')
    compound = models.TextField(blank=False, verbose_name='Склад')
    ph = models.FloatField(null=True, verbose_name='PH')
    contraindications = models.CharField(max_length=300, default=
    '''Тільки для зовнішнього використання. Можлива алергія або чутливість до компонентів. 
        Перед використанням зробити патч-тест.''', verbose_name='Протипоказання')
    storage_conditions = models.CharField(max_length=300, default=
    '''Зберігати в темному, сухому, прохолодному місці, недоступному для дітей, в закритій ємності за температури від +5 ℃ до + 25 ℃.''', 
    verbose_name='Умови зберігання')
    age_category = models.CharField(max_length=100, choices=AGES, verbose_name='Вікова категорія')
    expiration_date = models.CharField(max_length=300, default=
    '''24 міс. з моменту виготовлення, 12 міс. після початку використання.''', verbose_name='Термін придатності') 

    class Meta:
        verbose_name = 'Деталі продукту'
        verbose_name_plural = 'Деталі продуктів'


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks',verbose_name='Продукт')
    author_name = models.CharField(max_length=100, verbose_name="Iм'я")
    feedback = models.TextField(blank = False, verbose_name='Відгук')
    date_create = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True, verbose_name='Відображено')

    def __str__(self):
        return self.feedback

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-date_create']

class Question(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'Товар', related_name='questions')
    author_name = models.CharField(max_length=100, verbose_name="Ім'я")
    email = models.EmailField(verbose_name='Електронна пошта')
    question = models.TextField(blank=False, verbose_name='Питання')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    display = models.BooleanField(default=True, verbose_name='Відображено')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'
        ordering = ['-date_create']


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, verbose_name='Питання', related_name='answer', primary_key = True)
    answer = models.TextField(blank = False, verbose_name='Відповідь')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Відповідь на запитання'
        verbose_name_plural = 'Відповіді на запитання'
        ordering = ['-date_create']