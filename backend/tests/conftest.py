import random

import pytest
from django.urls import reverse


pytest_plugins = 'tests.factories'


@pytest.fixture()
@pytest.mark.django_db
def login_user(client, user):
    authorization_code = random.randint(1000, 9999)

    user.authorization_code = authorization_code
    user.save()

    response = client.post(reverse('auth:auth-verify'),
                           data={"phone": user.phone, "authorization_code": authorization_code})

    return user, response.data.get('access')
