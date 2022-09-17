import re
from Account.authorization import GlobalAuth
from Account.utils.decorators import check_pk
from  Cosmetic.models import *
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
                 cba : str =None,
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
    
    if hTl :
        product = product.order_by('-price')
    
    if lTh :
        product = product.order_by('price')
    if abc :
        product = product.order_by('name')
    
    if cba :
        product = product.order_by('-name')

    if cba :
        product = product.order_by('-name')


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



@Product_Router.post("/Reviw", response=RateOut ,auth=GlobalAuth)
@check_pk
def Reviw(request,rate_in:RateIn):
    rate = Review.objects.create(**rate_in.dict() , user=User.objects.get(id=request.auth['pk']))
    return rate


@Order_Router.get("/cart",response=List[ItemOut])
@check_pk
def view_cart(request):
    cart_item = Item.objects.filter(user=User.objects.get(id=request.auth['pk']),ordered=False)
    return cart_item
    

@Order_Router.post("/add_to_cart",response={
    200:MessageOut,
    404: MessageOut
})
def add_or_update_cart(request,item_add:CreatItem):
    try:
        item = Item.objects.get(product_id = item_add.product_id ,user=User.objects.get(id=request.auth['pk']),
        ordered=False)
        if item_add.item_qty > 0:
            item_add.item_qty += item_add.item_qty
        item_add.save()
    except Item.DoesNotExist:
        if item_add.item_qty < 1:
            return 400, {'detail': 'Quantity Value Must be Greter Than Zero'}    
        item = Item.objects.create(**item_add.dict(),user=User.objects.get(id=request.auth['pk']))
    return 200, {'detail':'Added to cart successfully'}

@Order_Router.post("/reduce_qty",response={
    200:MessageOut,
    404: MessageOut
})
def reduce_or_delete_cart(request,iterm_id:int):
    item = Item.get_object_or_404(Item, id = iterm_id ,user=User.objects.get(id=request.auth['pk']),
         ordered=False)
    if item.item_qty >=2:
        item.item_qty -= item.item_qty
        item.save()
    else:
        item.delete()
        return 200,{'detail':' Item deleted!'}
    return 200, {'detail': 'Item quantity reduced successfully!'}

@Address_Router.post('cities', response={
    201: CityOut,
    400: MessageOut,
})
def create_city(request, city_in: CityIn):
    city = City(**city_in.dict())
    city.save()
    return 201, city