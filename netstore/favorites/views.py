from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from topikstore.models import *
from topikstore.utils import *


@require_POST
def favorites_add(request, product_pk):

    '''Добавляет продукт в список избранного'''

    if 'favorites_products' in request.session:
        if product_pk in request.session['favorites_products']:
            request.session['favorites_products'].remove(product_pk)
        request.session['favorites_products'].insert(0, product_pk)

        request.session.modified = True
        print(request.session['favorites_products'])
    else:
        request.session['favorites_products'] = [product_pk]
    
    #Обновление страницы на которой вызывается favorites_remove
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


@require_POST
def favorites_remove(request, product_pk):

    '''Удаляет продукт из списка избранного'''

    if 'favorites_products' in request.session:
        if product_pk in request.session['favorites_products']:
            request.session['favorites_products'].remove(product_pk)

        request.session.modified = True
    else:
        request.session['favorites_products'] = [product_pk]
    
    #Обновление страницы на которой вызывается favorites_remove
    return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))


def favorites_detail(request):

    '''Отображения списка избранного из сессии'''

    favorites_products = None

    if 'favorites_products' in request.session:
        favorites_products = Products.objects.filter(pk__in=request.session['favorites_products'])

    context = get_user_context(
        title = 'Обране',
        favorites_products = favorites_products,
    )

    return render(request, 'favorites/detail.html', context=context)