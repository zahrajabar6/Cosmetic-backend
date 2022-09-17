from decimal import Decimal
from Cosmetic.models import Product
from ninja import Schema
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageOut(Schema):
    detail: str


class UserIn(Schema):
    email: str
    first_name: str
    last_name: str
    phone: str =None
    password: int


class UserOut(Schema):
    email: str
    phone: str =None


class ProductIn(Schema):
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal
    category: str
    brand: str
    is_active: bool


class ProductOut(Schema):
    id: int
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal
    # brand: 'BrandOut'=None
    is_active: bool


class CategoryIn(Schema):
    parent_id: int
    name: str
    description: str = None
    is_active: bool


class CategoryOut(Schema):
    id: int
    parent: 'CategoryOut' = None
    name: str
    is_active: bool


CategoryOut.update_forward_refs()


class BrandIn(Schema):
    name: str

# class BrandOut(Schema):
#     brand_id: int 
#     name: str

class ColorIn(Schema):
    product_name: str
    color: str
    image_url: str


class ColorOut(Schema):
    color: str
    image_url: str


class CityIn(Schema):
    name: str

class CityOut(CityIn):
    pass


class AddressIn(Schema):
    user_id: int
    address: str
    city: CityIn
    phone: str


class AddressOut(Schema):
    user: UserOut
    address: str
    city: CityIn


class OrderIn(Schema):
    user_id: int
    address: str
    total: Decimal
    status: str
    ordered: bool
    item: str


class OrderOut(Schema):
    user: UserOut
    address: AddressOut
    total: Decimal
    item: str


class ItemIn(Schema):
    user_id: int
    product: str
    item_qty: int
    ordered: bool

class CreatItem(Schema):
    product_id: int
    item_qty: int

class ItemOut(Schema):
    id: int
    user: UserOut
    product: ProductOut
    item_qty: int
    ordered: bool 

class RateIn(Schema):
    product_id : int 
    rate : int 

class RateOut(Schema):
    user : UserOut
    product:ProductOut
    rate: int