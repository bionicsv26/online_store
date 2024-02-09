from market.cart.cart import Cart
from market.sellers.models import SellerProduct


def create_json_cart(cart):
    cart_json = {}
    for item in cart:
        product_id = item['product']
        cart_json.update({product_id.pk: item['quantity']})

    return cart_json


def rebuild_cart(session, json_cart):
    cart = Cart(session)
    for product_id in json_cart:
        try:
            product = SellerProduct.objects.get(pk=int(product_id))
            cart.add(product, amount=json_cart[product_id])
        except SellerProduct.DoesNotExist:
            pass

