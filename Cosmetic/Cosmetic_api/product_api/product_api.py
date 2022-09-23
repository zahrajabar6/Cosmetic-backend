from Account.authorization import GlobalAuth
from Cosmetic.models import *
from Cosmetic.schemas import *
from django.db.models import Q
from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

Product_Router = Router(tags=['Product'])


@Product_Router.get("/list-products", response={
    200: List[ProductOut],
    404: MessageOut
})
def all_products(request, *,
                 query: str = None,
                 price_from: int = None,
                 price_to: int = None,
                 ascending: str = None,
                 descending: str = None,
                 abc: str = None,
                 cba: str = None,
                 ):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    if not products:
        return 404, {'detail': 'No Products found'}
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(brand__brand_name__icontains=query)
        )

    if price_from:
        products = products.filter(price__gte=price_from)

    if price_to:
        products = products.filter(price__lte=price_to)

    if ascending:
        products = products.order_by('-price')

    if descending:
        products = products.order_by('price')
    if abc:
        products = products.order_by('name')

    if cba:
        products = products.order_by('-name')

    return products


@Product_Router.get(f"/products", response={
    200: List[ProductOut],
    404: MessageOut
})
def product(request, product_id: int):
    products = Product.objects.filter(id=product_id).select_related('category', 'brand')
    if not products:
        return 404, {'detail': f'Product with id {product_id} does not exist'}
    return products


@Product_Router.get(f"/list_favorite", response={
    200: List[ProductOut],
    404: MessageOut
})
def list_favorite(request):
    products = Product.objects.filter(is_favorite=True).filter(is_active=True).select_related('category', 'brand')
    if not products:
        return 404, {'detail': 'No Products found'}
    return products


@Product_Router.put(f"/set_favorite", response={
    200: MessageOut,
    404: MessageOut
})
def set_favorite(request, id: int):
    product = get_object_or_404(Product, id=id)
    if not product:
        return 404, {'detail': f'Product with id {id} does not exist'}
    product.is_favorite = True
    product.save()
    return 200, {'detail': f'Product with id {id} set to favorite'}


@Product_Router.put(f"/Remove_favorite", response={
    200: MessageOut,
    404: MessageOut
})
def remove_favorite(request, id: int):
    product = get_object_or_404(Product, id=id)
    if not product:
        return 404, {'detail': f'Product with id {id} does not exist'}
    product.is_favorite = False
    product.save()
    return 200, {'detail': f'Product with id {id} remove from favorite'}

# @Product_Router.get(f"/list_category", response={
#     200: List[CategoryOut],
#     404: MessageOut
# })
# def categories(request):
#     categories = Category.objects.filter(is_active=True)
#     if not categories:
#         return 404, {'detail': f'categories not exist'}
#     return categories


# @Product_Router.get("/list-categories", response={
#     200: List[ProductOut],
#     404: MessageOut
# })
# def all_categories(request, *,
#                    ascending: str = None,
#                    descending: str = None,
#                    abc: str = None,
#                    cba: str = None,
#                    ):
#     products = Product.objects.filter(is_active=True).order_by('category').select_related('brand')
#     if not products:
#         return 404, {'detail': 'No Products found'}
#     if ascending:
#         products = products.order_by('-price')
#
#     if descending:
#         products = products.order_by('price')
#
#     if abc:
#         products = products.order_by('name')
#
#     if cba:
#         products = products.order_by('-name')
#
#     return products
