from .cart import Cart
from topikstore.models import *

'''Процессоры контекста - это функции, которые получают текущий HttpRequest 
   в качестве аргумента и возвращают dict данных для добавления в контекст визуализации.
   Их основное использование - добавление общих данных, используемых всеми шаблонами, 
   в контекст без повторения кода в каждом представлении.'''

def cart(request):
      favorites_products = None
      if 'favorites_products' in request.session:
            favorites_products = Product.objects.select_related('category', 'subcategory').filter(pk__in=request.session['favorites_products'])
      
      return {
         'cart': Cart(request), 
         'favorites_products': favorites_products
      }