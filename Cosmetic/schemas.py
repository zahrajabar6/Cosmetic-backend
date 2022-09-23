from decimal import Decimal
from ninja import Schema
from django.contrib.auth import get_user_model

from Account.schemas import AccountOut

User = get_user_model()


class MessageOut(Schema):
    detail: str


class CategoryIn(Schema):
    parent_id: int
    name: str
    description: str = None
    is_active: bool


class BrandOut(Schema):
    id: int
    brand_name: str


class CategoryOut(Schema):
    id: int
    parent: 'CategoryOut' = None
    name: str
    is_active: bool


CategoryOut.update_forward_refs()


class ProductIn(Schema):
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal
    color: str
    imageUrl: str
    category_id: int
    brand_id: int
    is_active: bool


class ProductOut(ProductIn):
    id: int
    name: str
    description: str = None
    ingredient: str = None
    price: Decimal
    discounted_price: Decimal
    color: str
    imageUrl: str
    brand: BrandOut = None
    category: CategoryOut = None
    is_active: bool


class OrderIn(Schema):
    user_id: int
    total: Decimal
    status: str
    ordered: bool
    item: str


class OrderOut(Schema):
    user: AccountOut
    total: Decimal
    item: str


class ItemIn(Schema):
    user_id: int
    product: str
    item_qty: int
    ordered: bool


class CreateItem(Schema):
    product_id: int
    item_qty: int


class ItemOut(Schema):
    id: int
    user: AccountOut
    product: ProductOut
    item_qty: int
    ordered: bool


class RateIn(Schema):
    product_id: int
    rate: int


class RateOut(Schema):
    user: AccountOut
    product_id: int
    rate: int
