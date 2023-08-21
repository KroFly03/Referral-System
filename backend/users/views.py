from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserRegisterSerializer, UserLoginSerializer, VerifyCodeSerializer, UserDetailSerializer, \
    ActivateInviteCodeSerializer, UserListSerializer

USER_MODEL = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = UserRegisterSerializer
    authentication_classes = []


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.create(serializer.validated_data), status=status.HTTP_201_CREATED)


class VerifyCodeView(APIView):
    serializer_class = VerifyCodeSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.create(serializer.validated_data), status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user


class ActivateInviteCodeView(generics.UpdateAPIView):
    serializer_class = ActivateInviteCodeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return USER_MODEL.objects.filter(activated_invite_code=self.request.user.invite_code)
