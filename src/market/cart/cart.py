from decimal import Decimal
from django.contrib import messages
from django.conf import settings
from django.http import HttpRequest
from market.sellers.models import SellerProduct


class Cart:
    def __init__(self, request: HttpRequest):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        product_ids = self.cart.keys()
        products = SellerProduct.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * int(item['quantity'])
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине
        """
        return sum(int(item['quantity']) for item in self.cart.values())
    

    def add(self, product: SellerProduct, amount: str):
        """
        Добавить товар в корзину.
        """
        product_id = str(product.id)
        product_stock = product.stock

        if product_stock >= int(amount):
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': amount,
                                         'price': str(product.price)}
            else:
                self.cart[product_id]['quantity'] = amount
        else:
            messages.error(self.request, f'У продавца только {product_stock} товаров')
        self.save()

    def save(self):
        """
        Пометить сеанс как "измененный", чтобы обеспечить его сохранение.
        """
        self.session.modified = True

    def remove(self, product_id: str) -> None:
        """
        Удалить товар из корзины.
        """
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Получить итоговую сумму корзины.
        """
        return sum(Decimal(item['price']) * int(item['quantity'])
                   for item in self.cart.values())
    
    def clear(self):
        """
        удалить корзину из сеанса 
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()