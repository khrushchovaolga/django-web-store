#Для отображение цены в той же единице, что и указано
import copy
from decimal import Decimal
from django.conf import settings
from topikstore.models import Product

class Cart(object):
    
    def __init__(self, request):

        '''Инициализация корзины'''

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #сохранить ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1,update_quantity=False):

        '''Метод для добавления товара в корзину
        update_quantity=False - добавить к существующему'''

        product_pk = str(product.pk)
        if product_pk not in self.cart:
            self.cart[product_pk] = {'quantity': 0, 
                                    'price': str(product.price),}
        #Обновление кол-ва товара
        if update_quantity:
            self.cart[product_pk]['quantity'] = quantity
        else:
            self.cart[product_pk]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):

        '''Удаление товара из корзины'''

        product_pk = str(product.pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
            self.save()

    def __iter__(self):

        '''Для перебора товаров в корзине и получения из БД'''

        product_ids = self.cart.keys()
        #получаем товары и добавляем их в корзину
        products = Product.objects.filter(id__in=product_ids, available=True)
        print(self.cart)
        #cart = copy.deepcopy(self.cart)
        cart = self.cart.copy()
        print(cart)
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):

        '''Подсчет товаров в корзине'''

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):

        '''Подсчет общей суммы'''

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):

        '''Очищение корзины в сессии'''

        del self.session[settings.CART_SESSION_ID]
        self.save()