from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth.models import User  # This is a builtIn model provided by the Django itself
from rest_framework.authtoken.models import Token


#  For each model, we will create a new serializer as below

class UserSerializer(serializers.ModelSerializer):
    class Meta:  # Here we can decide what will be there inside our serializer
        model = User  # Here we are telling the serializer, which model we are using
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}  # We are passing extra things to the field
        # password where it will be write_only which means we won't be able to see it, and it will be required if we
        # want to register

    # Here self is nothing, but the current data and validated_data means it is the data coming from the request that
    # are meeting our requirements for our Model for the user
    def create(self, validated_data):  # This create method is already included, but we are overwriting with our own
        # version of it
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:  # Here we can decide what will be there inside our serializer
        model = Movie  # Here we are telling the serializer, which model we are using
        fields = ('id', 'title', 'description', 'no_of_ratings', 'avg_rating')  # Here id is added automatically by
        # Django
        # In the above, we are telling the serializer which fields we are using. In the above fields there is a
        # 'no_of_ratings' field is there which is a function available on our movie which is in models.py file


class RatingSerializer(serializers.ModelSerializer):
    class Meta:  # Here we can decide what will be there inside our serializer
        model = Rating
        fields = ('id', 'stars', 'user', 'movie')  # Here id is added automatically by Django
