from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from topikstore.models import *
from topikstore.utils import *

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Products, pk=product_pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


@require_POST
def cart_remove(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Products, pk=product_pk)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True,
        })
    context = get_user_context(
        title = 'Кошик',
        cart = cart
    )
    return render(request, 'cart/detail.html', context=context)