import re
from Account.authorization import GlobalAuth
from Account.utils.decorators import check_pk
from Cosmetic.models import *
from Cosmetic.schemas import *
from django.db.models import Q
from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from django.contrib.auth import get_user_model

Product_Router = Router(tags=['Product'])
Address_Router = Router(tags=['Address'])
Order_Router = Router(tags=['Order'])

User = get_user_model()


@Product_Router.get("/list-products", response={
    200: List[ProductOut],
    404: MessageOut
})
def all_products(request, *,
                 query: str = None,
                 price_from: int = None,
                 price_to: int = None,
                 ascending: str = None,
                 discending: str = None,
                 abc: str = None,
                 cba: str = None,
                 ):

    product = Product.objects.filter(is_active=True).select_related('category', 'brand')
    if not product:
        return 404, {'detail': 'No Products found'}
    if query:
        product = product.filter(
            Q(name__icontains=query) | Q(brand__brand_name__icontains=query)
        )

    if price_from:
        product = product.filter(price__gte=price_from)

    if price_to:
        product = product.filter(price__lte=price_to)

    if ascending:
        product = product.order_by('-price')

    if discending:
        product = product.order_by('price')
    if abc:
        product = product.order_by('name')

    if cba:
        product = product.order_by('-name')

    return product

# @Product_Router.get("/product_rate")
# def rate_product(request ):

@Product_Router.get("/product", response={
    200: List[ProductOut],
    404: MessageOut
})
def product(request, id: int):
    product = Product.objects.filter(id=id).select_related('category', 'brand')
    if not product:
        return 404, {'detail': f'Account with id {id} does not exist'}
    return product


@Product_Router.post("/Reviw", response={
    200: RateOut,
    404: MessageOut}, auth=GlobalAuth())
def Reviw(request, rate_in: RateIn):
    return Review.objects.create(**rate_in.dict(), user=User.objects.get(id=request.auth['pk']))


@Order_Router.get("/cart", response={
    200:List[ItemOut],
    404: MessageOut
}, auth=GlobalAuth())
def view_cart(request):
    cart_item = Item.objects.filter(user=User.objects.get(id=request.auth['pk']), ordered=False)

    if not cart_item:
        return 404,{'detail': 'No Items In The Cart,Take your time and enjoy'}
    return 200, cart_item


@Order_Router.post("/add_to_cart", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def add_or_update_cart(request, item_add: CreatItem):
    try:
        item = Item.objects.get(product_id=item_add.product_id, user=User.objects.get(id=request.auth['pk']),
                                ordered=False)
        print(item.item_qty)
        if item_add.item_qty > 0:
            item.item_qty += item_add.item_qty
        item.save()
        print(item.item_qty)
    except Item.DoesNotExist:
        if item_add.item_qty < 1:
            return 400, {'detail': 'Quantity Value Must be Greter Than Zero'}
        item = Item.objects.create(**item_add.dict(), user=User.objects.get(id=request.auth['pk']))
    return 200, {'detail': 'Added to cart successfully'}


@Order_Router.post("/reduce_qty", response={
    200: MessageOut,
    404: MessageOut
}, auth=GlobalAuth())
def reduce_or_delete_cart(request, item_id: int):
    item = get_object_or_404(Item, id=item_id, user=User.objects.get(id=request.auth['pk']), ordered=False)
    if item.item_qty <= 1:
        item.delete()
        return 200, {'detail': 'Item deleted!'}
    item.item_qty -= 1
    item.save()

    return 200, {'detail': 'Item quantity reduced successfully!'}


@Address_Router.post('cities', response={
    201: CityOut,
    400: MessageOut,
})
def create_city(request, city_in: CityIn):
    city = City(**city_in.dict())
    city.save()
    return 201, city
