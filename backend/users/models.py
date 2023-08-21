import random
import string

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$',
        message='Номер телефона должен быть в формате: +7 (999) 123-45-67.'
    )
    
    username = None
    email = None
    password = None
    last_login = None
    groups = None
    user_permissions = None
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фаммлия', max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=30, validators=[phone_regex], unique=True)
    authorization_code = models.CharField(max_length=4, blank=True, null=True, unique=True)
    code_generation_time = models.DateTimeField(blank=True, null=True)
    invite_code = models.CharField(blank=True, null=True, unique=True)
    activated_invite_code = models.CharField(blank=True, null=True)
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def generate_code(self):
        while True:
            authorization_code = ''.join(str(random.randint(0, 9)) for _ in range(4))
            if not User.objects.filter(authorization_code=authorization_code).exists():
                self.authorization_code = authorization_code
                break

        self.code_generation_time = timezone.now()
        self.save()

        return self.authorization_code

    def clear_code(self):
        self.authorization_code = None
        self.code_generation_time = None
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                invite_code = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(6))
                if not User.objects.filter(invite_code=invite_code).exists():
                    self.invite_code = invite_code
                    break
        super().save(*args, **kwargs)
