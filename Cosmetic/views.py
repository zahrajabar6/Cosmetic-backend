from  Cosmetic.models import *
from Cosmetic.schemas import *
from django.db.models import Q
from ninja import Router
from typing import List
from django.contrib.auth import get_user_model

Product_Router = Router(tags=['Product'])
Address_Router = Router(tags=['Product'])
Order_Router = Router(tags=['Product'])


User = get_user_model()


@Product_Router.get("/list-products",response={
    200: List[ProductOut],
    404: MessageOut
    })
def all_products(request, *,
                 query: str = None,
                #  brand: str = None,
                 price_from: int = None,
                 price_to: int = None,
                 hTl: str = None,
                 lTh: str = None,
                 abc : str =None,
                 cba : str =None 

                 ):
    product = Product.objects.filter(is_active=True).select_related('category','brand')
    if not product:
        return 404, {'detail': 'No Products found'}
    if query:
        product = product.filter(
            Q(name__icontains=query) | Q(brand__name__icontains=query)
        )
    # if brand:
    #     b=Brand.objects.filter(name = brand)
    #     product = product.filter(b_id = brand)
    
    if price_from:
        product= product.filter(price__gte=price_from)

    if price_to:
        product = product.filter(price__lte=price_to)
    
    # if hTl :
    #     product = product.order_by('-price')
    
    # if lTh :
    #     product = product.order_by('price')
    # if abc :
    #     product = product.order_by('name')
    
    # if cba :
    #     product = product.order_by('-name')


    return product

@Product_Router.get("/product",response={
    200 : List[ProductOut],
    404 : MessageOut
    })
def product(request, id:int):
    product = Product.objects.filter(id = id).select_related('category','brand')
    if not product:
        return 404, {'detail': f'Account with id {id} does not exist'}
    return product

@Order_Router.get("/cart",response=List[ItemOut])
def view_cart(request):
    cart_item = Item.objects.filter(ordered=False)
    return cart_item
    
@Address_Router.post('cities', response={
    201: CityOut,
    400: MessageOut,
})
def create_city(request, city_in: CityIn):
    city = City(**city_in.dict())
    city.save()
    return 201, city