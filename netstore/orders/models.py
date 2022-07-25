from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from topikstore.models import *


class Cities(models.Model):
    city = models.CharField(max_length=250, verbose_name=_('City'))
    is_public = models.BooleanField(default=True, verbose_name=_('Is public'))

    def __str__(self):
        return self.city

    class Meta:
        ordering = ('-city', )
        verbose_name = _('City')
        verbose_name_plural = _('Cities')


class Order(models.Model):

    posts = (
        ('Nova Poshta', 'Нова пошта'),
        ('Ukrposhta' ,'Укрпошта'),
        ('Justin', 'Justin'),
        ('Meets' ,'Meets'),
    )

    STATUS = (
        ('New', _('New')),
        ('In prosessing', _('In prosessing')),
        ('Awaiting delivery', _('Awaiting delivery')),
        ('Received', _('Received')),
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name=_('Customer'))
    first_name = models.CharField(max_length=50, verbose_name=_("Customer name"))
    last_name = models.CharField(max_length=50, verbose_name=_('Surname'))
    number = models.CharField(max_length=12, verbose_name=_('Number'))
    email = models.EmailField(verbose_name=_('Email'))
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, verbose_name=_('City'))
    post = models.CharField(choices=posts, max_length=150, verbose_name=_('Post'))
    number_of_post = models.CharField(max_length=15, verbose_name=_("Post number"))
    call = models.BooleanField(default=True, verbose_name=_('Call me'))
    data_create = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    data_update = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))
    status = models.CharField(max_length=250, default=_('New'), choices=STATUS, verbose_name=_('Status'))

class Meta:
    ordering = ('-data_create', )
    verbose_name = _('Order')
    verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{_("Order")} {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Product'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity