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


@Product_Router.get("/products", response={
    200: List[ProductOut],
    404: MessageOut
})
def product(request, product_id: int):
    products = Product.objects.filter(id=product_id).select_related('category', 'brand')
    if not products:
        return 404, {'detail': f'Account with id {product_id} does not exist'}
    return products

@Product_Router.post('create-product',response=ProductOut,
                     auth=GlobalAuth())
def create_product(request ,product_in:ProductIn):
    product = Product.objects.create(**product_in.dict())
    product.save()
    return product

@Product_Router.post("/Set_rate", response={
    200: RateOut,
    400: MessageOut}, auth=GlobalAuth())
def rate(request, rate_in: RateIn):
    review = Rate.objects.create(**rate_in.dict(), user=User.objects.get(id=request.auth['pk']))
    return  200 ,review

@Product_Router.post("/Product_rates", response={
    200: List[RateOut],
    404: MessageOut}, auth=GlobalAuth())
def product_reviews(request, id : int):
    products = Rate.objects.all().filter( product_id = id)
    return 200, products


'''
    ___1___
    if rate_in.rate > 5:
        return 400 ,  {'detail': 'Oh Sorry,the rating can not be higher than 5 '}
    review = get_object_or_404(Review,product_id = rate_in.product_id , user=User.objects.get(id=request.auth['pk']))
    if not review :
        review = Review.objects.create(**rate_in.dict(), user=User.objects.get(id=request.auth['pk']))
        return 200, review
    review.rate = rate_in.rate
    review.save()
    return 200 , review
    ___2___
    review = get_object_or_404(Review, product_id=rate_in.product_id, user=User.objects.get(id=request.auth['pk']))
    reviews = Review.objects.filter(user=User.objects.get(id=request.auth['pk']))
    if review in reviews:
        review.rate = rate_in.rate
        review.save()
        print(review)
        return 200, review
    review = Review.objects.create(**rate_in.dict(), user=User.objects.get(id=request.auth['pk']))
    return 200, review
'''