from django.shortcuts import get_object_or_404

from Account.authorization import GlobalAuth
from Cosmetic.models import *
from Cosmetic.schemas import *
from ninja import Router
from typing import List
from django.contrib.auth import get_user_model

User = get_user_model()

Rate_Router = Router(tags=['Rate'])


@Rate_Router.post("/Set_rate", response={
    200: RateOut,
    400: MessageOut}, auth=GlobalAuth())
def rate(request, rate_in: RateIn):
    user = User.objects.get(id=request.auth['pk'])
    if rate_in.rate not in range(0, 6):
        return 400, {'detail': 'Oh Sorry,the rating can be between 0 and 5 '}
    try:
        user_in_rate = user.rates.get(product_id=rate_in.product_id)
        if user_in_rate:
            user_in_rate.rate = rate_in.rate
            user_in_rate.save()
            return 200, {'detail': 'Rate is updated'}
    except Rate.DoesNotExist:
        review = Rate.objects.create(**rate_in.dict(), user=user)
        return 200, {'detail': 'Rate in created'}


@Rate_Router.get(f"/Product_avg_rate", response={
    200: RateOut
}, auth=GlobalAuth())
def get_avg_rate(request, product_id: int):
    product = Product.objects.get(id=product_id)
    rates = product.rates.all()
    rating = rates.count()
    for no_rate in rates:
        no_rate.rate += no_rate.rate
    avg_rate = no_rate.rate / rating
    return 200, {
        'product_id': product_id,
        'rate': round(avg_rate, 2)
    }
