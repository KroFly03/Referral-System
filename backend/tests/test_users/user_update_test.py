import json
from types import NoneType

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestDetailUserView:
    base_url = 'users:users-me'

    def test_return_correct_data_keys(self, client, login_user):
        _, access_token = login_user

        response = client.patch(reverse('users:users-me'), HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert list(response.data.keys()) == ['date_joined', 'first_name', 'last_name', 'phone', 'invite_code',
                                              'activated_invite_code']

    def test_correct_status_code(self, client, login_user):
        _, access_token = login_user

        response = client.patch(reverse('users:users-me'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json().get('detail') == 'Учетные данные не были предоставлены.'

        response = client.patch(reverse('users:users-me'), HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert response.status_code == status.HTTP_200_OK

    def test_correct_data_type(self, client, login_user):
        _, access_token = login_user

        response = client.patch(reverse('users:users-me'), HTTP_AUTHORIZATION=f'Bearer {access_token}')

        assert [type(value) for value in response.data.values()] == [str, str, str, str, str, NoneType]

    def test_correct_update(self, client, login_user):
        _, access_token = login_user

        update_data = {
            'first_name': 'test',
            'last_name': 'test',
        }

        response = client.patch(reverse('users:users-me'), data=json.dumps(update_data),
                                HTTP_AUTHORIZATION=f'Bearer {access_token}', content_type='application/json')

        for field in update_data.keys():
            assert response.data.get(field) == update_data.get(field)
