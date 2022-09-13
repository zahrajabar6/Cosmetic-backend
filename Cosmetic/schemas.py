from decimal import Decimal
from ninja import Schema


class UserIn(Schema):
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    password: int


class UserOut(Schema):
    username: str
    phone: str


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


class ColorIn(Schema):
    product_name: str
    color: str
    image_url: str


class ColorOut(Schema):
    color: str
    image_url: str


class CityIn(Schema):
    name: str


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


class ItemOut(Schema):
    id: int
    user: UserOut
    product: ProductOut
    item_qty: int
