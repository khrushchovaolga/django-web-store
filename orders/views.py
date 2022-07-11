from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):

    '''Получаем текущую корзину из сессии'''

    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
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
            return render(request, 'orders/created.html', {
                'order': order
            })
    else:
        form = OrderCreateForm
    return render(request, 'orders/create.html', {
        'cart': cart, 'form': form,
    })