import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestAuthRegisterView:
    url = reverse('auth:auth-register')
    initial_data = {
        'first_name': 'test',
        'last_name': 'test',
        'phone': '+7 (999) 888-77-66',
    }

    def test_return_correct_data_keys(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert response.data.keys() == self.initial_data.keys()

    def test_correct_status_code(self, client):
        response = client.post(self.url, data={}, content_type='application/json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_correct_return_data_type(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        assert [type(value) for value in response.data.values()] == [str, str, str]

    def test_correct_require_field_validation(self, client):
        response = client.post(self.url, data={}, content_type='application/json')

        assert response.data.get('phone') == ['Обязательное поле.']

    def test_correct_phone_validation(self, client):
        incorrect_initial_data = {
            'first_name': 'test',
            'last_name': 'test',
            'phone': '+79998887766',
        }

        response = client.post(self.url, data=json.dumps(incorrect_initial_data), content_type='application/json')

        assert response.data.get('phone', None) == ['Номер телефона должен быть в формате: +7 (999) 123-45-67.']

    def test_correct_phone_unique(self, client, user):
        incorrect_initial_data = {
            'first_name': 'test',
            'last_name': 'test',
            'phone': user.phone,
        }

        response = client.post(self.url, data=json.dumps(incorrect_initial_data), content_type='application/json')

        assert response.data.get('phone', None) == ['Пользователь с таким Телефон уже существует.']

    def test_correct_register(self, client):
        response = client.post(self.url, data=json.dumps(self.initial_data), content_type='application/json')

        for field in self.initial_data.keys():
            assert response.data.get(field) == self.initial_data.get(field)
