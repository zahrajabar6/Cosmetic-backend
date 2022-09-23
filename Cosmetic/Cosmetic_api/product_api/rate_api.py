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
    review = Rate.objects.create(**rate_in.dict(), user=User.objects.get(id=request.auth['pk']))
    return 200, review


@Rate_Router.post(f"/Product_rates", response={
    200: List[RateOut],
    404: MessageOut}, auth= None)
def product_reviews(request, id: int):
    products = Rate.objects.all().filter(product_id=id)
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
