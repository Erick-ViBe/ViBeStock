from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken

from users.serializers import UserSerializer


class SignupAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [ AllowAny, ]
