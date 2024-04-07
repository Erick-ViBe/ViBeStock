from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user creation and obtain """

    class Meta:
        model = User
        fields = [ 'id', 'email', 'password' ]
        extra_kwargs = {
            'id': { 'read_only': True },
            'password': {
                'write_only': True,
                'min_length': 8,
            },
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for user authentication """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        min_length=8,
    )

    def validate(self, attrs):
        """ Validate and authenticate the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs

    
class ResponseTokenSerializer(serializers.ModelSerializer):
    """ Serializer for Token response """

    token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ['token']
