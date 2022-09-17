from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderStatusChoices(models.TextChoices):
    NEW ='NEW','New'
    PROCESSING = 'PROCESSING','Peoceeing'
    SHIPPED = 'SHIPPED','Shipped'
    COMPLETED = 'COMPLETED','Completed'
    REFUNDED = 'REFUNDED','Refunded'

class Product(models.Model):
    name = models.CharField(verbose_name='Product_Name', max_length=255)
    description = models.TextField('description', null=True, blank=True)
    ingredient = models.TextField('ingredient', null=True, blank=True)
    price = models.DecimalField('price', max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField('discounted price', max_digits=10, decimal_places=2,
                                           null=True,blank=True,default= 0)
    category = models.ForeignKey('Category', verbose_name='category', related_name='products',
                                 null=True,blank=True,
                                 on_delete=models.SET_NULL)
    brand = models.ForeignKey('Brand',on_delete=models.SET_NULL,
                                 null=True,blank=True)
    is_active = models.BooleanField('is active')

    def __str__(self):
        return f'{self.name}-{self.category}'
class Category(models.Model):
    parent = models.ForeignKey('self',verbose_name='parent',related_name='children',null=True,blank=True,
                               on_delete=models.CASCADE)
    name = models.CharField('name', max_length=255)
    description = models.TextField('description',null=True , blank=True)
    is_active = models.BooleanField('is active')

    def __str__(self):
        if self.parent:
            return f'{self.parent}-{self.name}'
        return f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Color(models.Model):
    productName = models.ForeignKey('Product',verbose_name='Product_Name',on_delete=models.SET_NULL,null=True)
    color = models.CharField(max_length=50,verbose_name='Product_Color')
    imageUrl = models.URLField(max_length=255)

    def __str__(self):
        return f'{self.productName} - {self.color}'

class Brand(models.Model):
    Brand_Name = models.CharField(verbose_name='Brand_Name',max_length=200)

    def __str__(self):
        return self.Brand_Name

class City(models.Model):
    name = models.CharField('city', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='addresses', on_delete=models.CASCADE)
    address = models.CharField('address', max_length=255)
    city = models.ForeignKey('City', related_name='addresses', on_delete=models.CASCADE,null=True)
    phone = models.CharField('phone', max_length=255)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    def __str__(self):
        return f' {self.user}-{self.address} - {self.phone}'

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='orders', null=True, blank=True,
                             on_delete=models.CASCADE)
    address = models.ForeignKey('Address', verbose_name='address',related_name='orders', null=True, blank=True,
                                on_delete=models.CASCADE)
    total = models.DecimalField('total', blank=True, null=True, max_digits=1000, decimal_places=0)
    status = models.CharField('status', max_length=255, choices=OrderStatusChoices.choices)
    ordered = models.BooleanField('ordered')
    items = models.ManyToManyField('Item', verbose_name='items', related_name='orders')

    def __str__(self):
        return f'{self.total}'


class Item(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name='product',
                                on_delete=models.CASCADE)
    item_qty = models.IntegerField('item_qty')
    ordered = models.BooleanField('ordered', default=False)

    def __str__(self):
        return f'{self.user}-{self.product}-{self.item_qty}'

class Review(models.Model):
    user = models.ForeignKey(User,verbose_name='user',related_name='reviws',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='product',
                                on_delete=models.CASCADE)
    rate = models.IntegerField(default= 0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user}-{self.product}-{self.rate}'