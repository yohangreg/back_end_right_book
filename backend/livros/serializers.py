from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reviews, WishList

class ReviewsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='usuario.first_name', read_only=True)
    last_name = serializers.CharField(source='usuario.last_name', read_only=True)

    class Meta:
        model = Reviews
        fields = ['id', 'livro', 'nota', 'comentario', 'data_criacao', 'usuario', 'first_name', 'last_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        db_table = "Users" 

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['id', 'usuario', 'livro']
        db_table = "Wish_List"
