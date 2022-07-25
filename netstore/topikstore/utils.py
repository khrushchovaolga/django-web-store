from cart.forms import CartAddProductForm
from .models import *

def get_user_context(**kwargs):

    context = {}
    for key, value in kwargs.items():
        context[key] = value

    context.update({
        'categories': Categories.objects.prefetch_related("subcats").filter(is_public=True),
        'cart_product_form': CartAddProductForm(),
    })
    return context