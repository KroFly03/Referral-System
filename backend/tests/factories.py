import random

import factory.django
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import datetime
from pytest_factoryboy import register

USER_MODEL = get_user_model()


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = (f'+7 ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-'
             f'{random.randint(10, 99)}')
    authorization_code = None
    code_generation_time = datetime.now()
