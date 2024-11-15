from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie, Rating
from django.contrib.auth.models import User  # This is a builtIn model provided by the Django itself
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


# Create your views here.
# We will create views for each of the serializers that we have created in serializers.py file

# We are creating view sets using builtIn django-rest-framework view sets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # This query set tells what set of records you want to use from the data
    # base and in the above case, we are using all the Movies
    serializer_class = UserSerializer  # What serializer we will be using for the above MovieViewSet


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()  # This query set tells what set of records you want to use from the data
    # base and in the above case, we are using all the Movies
    serializer_class = MovieSerializer  # What serializer we will be using for the above MovieViewSet
    authentication_classes = (TokenAuthentication,)  # We are using token_authentication for this MovieViewSet
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])  # Here we are decorating our method with some extra values
    # we are saying detail=True which means this is not going to be available on movies/. So detail=True
    # means one specific movie and detail=False means on a list of all the movies and the methods are that
    # it will accept
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:  # Here request.data means the req.body that we will send in the postman
            # API, Basically we have to pass the stars in the body of postman API when we are testing this
            # route.
            movie = Movie.objects.get(id=pk)  # We are selecting the movie from our database based on the
            # primary key that we have passed into the postman request
            # print(pk)  # It will print 1(id of the movie) to the console whenever we have tested this
            # # request on postman, Here PK stands for a primary key which is the ID of the movie that we
            # # have passed in the postman request
            stars = request.data['stars']  # As stars are there in the request.data
            print('stars', stars)
            user = request.user  # Here we are getting the user from token_authentication
            print('user', user)
            # user = User.objects.get(id=1)  # This user is fixed, and this is a static way of doing
            ##### There is another way of doing it? Refer below #####
            # whenever we are using the above rate_movie() function , We can also request it to have that
            # userId in the method itself, user = request.user => This is very robust because it will work
            # for the login user but if we would like to allow other people who are not logging into our
            # system to make us some kind of rating, then we have to store it. But we kind of designed
            # in this way in our models where we say you have to pass the user, the user has to be unique
            # along with the movie. So at the moment when you decided that you will pass the user, you need
            # to actually create the application in the way where the user will be extracted from the person
            # who is calling the "rate_movie()" function. So if I am logging now and I will try to do the
            # rating, then my user will be passed to the above "rate_movie()" method
            print('user', user.username)
            # Here we have two options where first we will check whether the rating already exists (or) not?
            # So if we have something in our database with the movie and stars, if we do have it, then we will
            # update it and if we don't have it we will create a new rating
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)  # we are selecting the serializer with the
                # updated rating when we save it, then we had more information into our response, and then we
                # will pass the response with http status 200
                response = {'message': 'Rating has been updated successfully', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)  # Here we are creating a new object
                # with the user,movie and star.
                serializer = RatingSerializer(rating, many=False)  # we are selecting the serializer with the
                # updated rating when we save it, then we had more information into our response, and then we
                # will pass the response with http status 200
                response = {'message': 'Rating has been created successfully', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            # print ('Movie title', movie.title)

        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


# If we are using ModelViewSet as below, then it will be open to everything which means it will be open to all the
# five methods, and if we want to stop using them, then we have to override as below with our own custom code as you
# can see we have written below our own custom code for the below update() and create builtIn methods of ModelViewSet
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Here we are overwriting the builtIn Django update method with our own version
    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update the rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create the rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
