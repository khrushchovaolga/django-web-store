from django.db import models
from topikstore.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    cities = (
        ('Dnipro', 'Dnipro'),
        ('Kiev', 'Kiev'),
        ('Kharkiv', 'Kharkiv'),
        ('Zaporizhya', 'Zaporizhya'),
    )

    posts = (
        ('Nova Poshta', 'Нова пошта'),
        ('Ukrposhta' ,'Укрпошта'),
        ('Justin', 'Justin'),
        ('Meets' ,'Meets'),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Користувач')
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    number = models.CharField(max_length=12, verbose_name='Номер телефону')
    email = models.EmailField(verbose_name='Електронна пошта')
    city = models.CharField(choices=cities, max_length=100, verbose_name='Місто')
    post = models.CharField(choices=posts, max_length=150, verbose_name='Пошта')
    number_of_post = models.CharField(max_length=15, verbose_name='Номер відділення:')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    data_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновлення')
    paid = models.BooleanField(default=False, verbose_name='Сплачено')

class Meta:
    ordering = ('-data_create', )
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity