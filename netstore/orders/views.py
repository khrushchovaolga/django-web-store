from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from topikstore.utils import *


def order_create(request):

    '''Получаем текущую корзину из сессии'''

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid() and len(cart) > 0:
            print('Get')
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity=item['quantity']
                )
            #очистка корзины после оформления заказа
            cart.clear()
            context = get_user_context(
                order = order,
                title = _('Замовлення успішно створено'),
            )
            return render(request, 'orders/created.html', context)
    else:
        form = OrderCreateForm

    context = get_user_context(
        cart = cart, 
        form = form,
        title = _('Оформлення замовлення'),
    )

    return render(request, 'orders/create.html', context)