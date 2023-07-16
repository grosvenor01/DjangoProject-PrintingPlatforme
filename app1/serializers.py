from rest_framework import serializers
from .models import * 
class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # the field will only be used for deserialization (when creating or updating an object
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = seller
        fields = "__all__"
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = reviews
        fields = "__all__"