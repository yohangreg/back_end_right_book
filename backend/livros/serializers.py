from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Reviews, WishList

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
        db_table = "Reviews" 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        db_table = "Users" 

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'
        db_table = "Wish_List"
