from copy import deepcopy
from decimal import Decimal
from django.contrib import messages
from django.conf import settings
from market.sellers.models import SellerProduct, Discount, DiscountType


class Cart:
    queryset = None

    def __init__(self, session):
        """
        Инициализация корзины
        """
        self.session = session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        discount_type, _ = DiscountType.objects.get_or_create(name='undiscounted')
        self.discount, _ = Discount.objects.get_or_create(type=discount_type)

        product_ids = self.cart.keys()
        self.queryset = SellerProduct.objects.select_related('discount', 'product').filter(id__in=product_ids)

    def __iter__(self):
        """
        Прокорутить товарные позиции корзины в цикле и
        получить товары из базы данных
        """
        cart = deepcopy(self.cart)
        for product in self.queryset:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product: SellerProduct, amount: int):
        """
        Добавить товар в корзину
        """
        product_id = str(product.id)
        product_stock = product.stock
        if amount < 1:
            self.remove(product_id)
            return

        if product_stock >= amount:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': amount,
                                         'price': str(product.price)}
            else:
                self.cart[product_id]['quantity'] = amount
        self.save()

    def save(self):
        """
        Пометить сеанс как "изменённый", чтобы обеспечить его сохранение.
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
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        """
        Удалить корзину из сеанса
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_discounted_cost(self) -> Decimal:
        """
        Получить стоимость корзины со скидкой
        """
        if len(self) >= self.discount.amount_products:
            return self.get_total_price() * Decimal(1 - self.discount.value / 100)
        return self.get_total_price()

    def get_total_discounted_seller_products_price(self) -> Decimal:
        """
        Получить суммарную стоимость всех продуктов со скидкой
        """
        return sum(
            seller_product.get('product').get_discounted_price() * seller_product.get('quantity')
            for seller_product in self
        )

    def get_priority_discounted_cost(self) -> Decimal:
        """
        Получить стоимость корзины с приоритетной скидкой
        """
        cart_discount_cost = self.get_discounted_cost()
        total_discounted_seller_products_price = self.get_total_discounted_seller_products_price()

        return min((cart_discount_cost, total_discounted_seller_products_price))

    def get_priority_discount_type(self) -> str:
        """
        Получить тип приоритетной скидки (скидка на корзину или суммарная скидка на все продукты)
        """
        cart_discount_cost = self.get_discounted_cost()
        total_discounted_seller_products_price = self.get_total_discounted_seller_products_price()

        if cart_discount_cost > total_discounted_seller_products_price:
            discount_type = 'products_discount'

        elif cart_discount_cost < total_discounted_seller_products_price:
            discount_type = 'cart_discount'

        else:
            discount_type = 'undiscounted'

        return discount_type
