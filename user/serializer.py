from rest_framework import serializers
from user.models import User
from borrowing.serializer import BorrowingSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserSerializer(serializers.ModelSerializer):
    
    count_borrowings = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'id', 'email', 'full_name', 'count_borrowings']

    def get_count_borrowings(self, obj):
        return obj.borrowing_set.filter(status='OUT').count()
    
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'full_name', 'id']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        
        
User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('username ou senha inválidas')

        if not user.check_password(password):
            raise serializers.ValidationError('username ou senha inválidas')

        if not user.is_active:
            raise serializers.ValidationError('Usuário inativo')

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data

    @classmethod
    def get_token(cls, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        return RefreshToken.for_user(user)
