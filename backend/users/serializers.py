from time import sleep

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

USER_MODEL = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('first_name', 'last_name', 'phone')


class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True, validators=[USER_MODEL.phone_regex])

    class Meta:
        model = USER_MODEL
        fields = ('phone',)

    def create(self, validated_data):
        user, _ = USER_MODEL.objects.get_or_create(phone=validated_data['phone'])
        sleep(2)
        code = user.generate_code()
        return {'code': f'Код авторизации отправлен. ({code})'}


class VerifyCodeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    authorization_code = serializers.CharField(required=True)

    class Meta:
        model = USER_MODEL
        fields = ('phone', 'authorization_code',)

    def create(self, validated_data):
        try:
            user = USER_MODEL.objects.get(phone=validated_data['phone'],
                                          authorization_code=validated_data['authorization_code'])

            if user.code_generation_time < timezone.now() - timezone.timedelta(minutes=5):
                raise ValidationError({'code': 'Время действие кода истекло.'})

            user.clear_code()

            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return {'access': access, 'refresh': str(refresh)}
        except USER_MODEL.DoesNotExist:
            raise ValidationError({'user': ['Неверные данные.']})


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('date_joined', 'first_name', 'last_name', 'phone', 'invite_code', 'activated_invite_code')
        read_only_fields = ('date_joined', 'phone', 'invite_code', 'activated_invite_code')


class UserListSerializer(UserLoginSerializer):
    pass


class ActivateInviteCodeSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(required=True)

    class Meta:
        model = USER_MODEL
        fields = ('invite_code',)

    def update(self, instance: USER_MODEL, validated_data):
        if not validated_data.get('invite_code'):
            raise ValidationError({'invite_code': ['Обязательное поле.']})

        invite_code = validated_data['invite_code']

        if not USER_MODEL.objects.filter(invite_code=invite_code).exists():
            raise ValidationError({'code': 'Данного инвайт кода не существует.'})

        if instance.activated_invite_code:
            raise ValidationError({'code': 'У Вас уже введен инвайт код.'})

        if instance.invite_code == invite_code:
            raise ValidationError({'code': 'Вы не можете вести свой инвайт код.'})

        instance.activated_invite_code = invite_code
        instance.save()

        return {'invite_code': invite_code}
