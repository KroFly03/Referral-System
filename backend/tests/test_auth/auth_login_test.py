import json
import re

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestAuthLoginView:
    url = reverse('auth:auth-login')
    initial_data = {
        'phone': '+7 (999) 888-77-66',
    }

    def test_return_correct_data_keys(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert list(response.data.keys()) == ['code']

    def test_correct_status_code(self, client):
        response = client.post(self.url, data={}, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_correct_return_data_type(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert [type(value) for value in response.data.values()] == [str]

    def test_correct_require_field_validation(self, client):
        response = client.post(self.url, data={}, content_type='application/json')

        assert response.data.get('phone') == ['Обязательное поле.']

    def test_correct_phone_validation(self, client):
        incorrect_initial_data = {
            'phone': '+79998887766',
        }

        response = client.post(self.url, data=json.dumps(incorrect_initial_data), content_type='application/json')

        assert response.data.get('phone', None) == ['Номер телефона должен быть в формате: +7 (999) 123-45-67.']

    def test_correct_new_user_login(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert re.sub(r'\d', '', response.data.get('code')) == 'Код авторизации отправлен. ()'

    def test_correct_login(self, client, user):
        response = client.post(self.url, data=json.dumps({'phone': user.phone}), content_type='application/json')

        assert re.sub(r'\d', '', response.data.get('code')) == 'Код авторизации отправлен. ()'

